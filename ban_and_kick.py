import time
import asyncio
from models.group_member_info import GroupInfoUser
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
)
from utils.utils import get_message_at, is_number
from services.log import logger
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER


__zx_plugin_name__ = "禁言/踢人 [Admin]"
__plugin_usage__ = """
usage：
    指令:
        ban [at] ? (Min)
        ban [at] 0 解除禁言
        kick [at] 踢
        kugm ?(default 10) 踢出不活跃用户 
""".strip()
__plugin_version__ = 0.1
__plugin_author__ = "YiJiuChow"
__plugin_settings__ = {
    "admin_level": 5,
}
__plugin_configs__ = {
    "BAN_LEVEL [LEVEL]": {
        "value": 5,
        "help": "ban/kick所需要的管理员权限等级",
        "default_value": 5,
    }
}


banuser = on_command("ban", aliases={"禁"}, priority=5, block=True)
kickuser = on_command("kick", aliases={"踢"}, priority=5, block=True)
kugm = on_command("kugm", priority=5, permission=SUPERUSER, block=True)


@banuser.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    try:
        baned_user = get_message_at(event.json())[0]
    except:
        logger.error(f"没有@需要被禁言的人")
        return
    msg = arg.extract_plain_text().strip()
    ban_time = 600
    if is_number(msg) and not (int(msg) < 0 or int(msg) > 60 * 24 * 29):
        ban_time = int(msg) * 60
    await bot.set_group_ban(group_id=event.group_id, user_id=baned_user, duration=ban_time)
    logger.info(
        f"ban_user group_id={event.group_id} user_id={baned_user} duration={ban_time}s")


@kickuser.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    try:
        kicked_user = get_message_at(event.json())[0]
    except:
        logger.error(f"没有@要踢的人")
        return
    if kicked_user:
        try:
            await bot.set_group_kick(group_id=event.group_id, user_id=kicked_user)
            logger.info(
                f"set_group_kick success group_id = {event.group_id}, user_id = {kicked_user}")
            await kickuser.send(message=f"{kicked_user} 被我送走了")
        except Exception as e:
            logger.error(f"set_group_kick failed {e}")


@kugm.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if not (await bot.get_group_member_info(user_id=bot.self_id, group_id=event.group_id, no_cache=True))["role"] in ["admin", "owner"]:
        await kugm.finish(message="机器人权限不足")
    msg = arg.extract_plain_text().strip()
    kicked_num = 10
    if is_number(msg) and not (int(msg) < 0 or int(msg) > 30):
        kicked_num = int(msg)
    # 群员列表
    gm_list = await GroupInfoUser.get_group_member_id_list(group_id=event.group_id)
    # 待踢列表
    member_list = []
    # 待踢成员计数
    kicked_count = 0
    now_time = int(time.time())
    for member_qq in gm_list:
        try:
            member = await bot.get_group_member_info(user_id=member_qq, group_id=event.group_id, no_cache=True)
        except:
            await GroupInfoUser.delete_member_info(user_qq=member_qq, group_id=event.group_id)
            continue
        if (now_time - int(member["last_sent_time"]) > 7777777) and int(member["level"]) < 30:
            member_list.append(member["user_id"])
            kicked_count += 1
        if kicked_count == kicked_num:
            break
    for qq in member_list:
        await bot.set_group_kick(group_id=event.group_id, user_id=qq)
        await GroupInfoUser.delete_member_info(user_qq=qq, group_id=event.group_id)
        logger.info(f"group_id={event.group_id} user_id={qq} 已踢")
        await asyncio.sleep(1)
    await kugm.finish(message=f"{','.join(str(i) for i in member_list)} 通通被我送走了捏")
