import asyncio
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from utils.utils import get_message_at, is_number
from services.log import logger
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from .model import GroupInfoUserByMe
from .data_source import get_kicked_list


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
    message_str = ""
    for member in await get_kicked_list(bot=bot, group_id=event.group_id, kicked_num=kicked_num):
        await bot.set_group_kick(group_id=event.group_id, user_id=member["user_id"])
        await GroupInfoUserByMe.delete_member_info(user_qq=member["user_id"], group_id=event.group_id)
        logger.info(f"{member} -> kicked")
        message_str += f"{member['user_id']} {(member['card'] if not member['card'] == '' else member['nickname'])}\n"
        await asyncio.sleep(1)
    await kugm.finish(message=f"{message_str} 通通被我送走了捏")
