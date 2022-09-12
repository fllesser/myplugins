from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, GroupIncreaseNoticeEvent
from utils.utils import get_message_at, is_number
from services.log import logger
from nonebot import on_command, on_notice
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from .data_source import kick_not_active_member

__zx_plugin_name__ = "禁言/踢人"
__plugin_usage__ = """
usage：
    指令:
        ban [at] ? (Min)
        ban [at] 0 解除禁言
        kick [at] 踢
        kugm ?(default 10) 踢出不活跃用户 
""".strip()
__plugin_type__ = ("其他",)
__plugin_cmd__ = ["ban", "kick", "kugm"]
__plugin_des__ = "禁/踢"

# 权限过滤
permission_filter = on_command(cmd="ban", aliases={"kick", "kugm"}, priority=1)

@permission_filter.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if (await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id, no_cache=True))["role"] == "member":
        permission_filter.block = True
        await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
        await permission_filter.finish(message="乱玩管理命令, 禁言一分钟")
    else:
        permission_filter.block = False    


banuser = on_command("ban", priority=5, block=True)
kickuser = on_command("kick", priority=5 , block=True)
kugm = on_command("kugm", priority=5, permission=SUPERUSER, block=True)
gm_increase = on_notice(priority=5, block=False)


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
    msg = arg.extract_plain_text().strip()
    kicked_num = 10
    if is_number(msg) and not (int(msg) < 0 or int(msg) > 30):
        kicked_num = int(msg)
    result = await kick_not_active_member(bot=bot,group_id=event.group_id,kicked_num=kicked_num)
    await kugm.finish(message=result)


@gm_increase.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    group_info = await bot.get_group_info(group_id=event.group_id, no_cache=True)
    # logger.info(f"该群当前人数 {group_info['member_count']}")
    if group_info["member_count"] == group_info["max_member_count"]:
        await bot.send_group_msg(
            message="检测到该群人数已满\n开始踢除不活跃用户\n当前规则:\n 1.超过三个月不发言\n 2.群活跃等级小于20",
            group_id=event.group_id)
        message_str = await kick_not_active_member(bot=bot,group_id=event.group_id,kicked_num=10)
        await gm_increase.finish(message=message_str)

