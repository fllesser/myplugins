from nonebot.adapters.onebot.v11 import (
    Bot, GroupMessageEvent, NoticeEvent, Message, GroupIncreaseNoticeEvent, GROUP_ADMIN, GROUP_OWNER
)
from nonebot import on_command, on_notice, on_message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot import get_driver

from utils.utils import is_number
from services.log import logger

from .data_source import kick_not_active_member, get_kicked_list, query_start_dict

__zx_plugin_name__ = "ban/kick/kugm"
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
__plugin_des__ = "ban/kick/kugm"

AUTO_KICK_RULE: str = '''检测到该群人数已满
当前规则:
 1.超过三个月不发言
 2.群活跃等级小于20(不太准确)
 3.没有头衔(发送 sgst 头衔名 即可授予自己头衔)
注:三条规则同时满足才有可能被踢'''.strip()

driver = get_driver()

# websocket连接后 初始化query_start
# @driver.on_bot_connect
# async def init_condition(bot: Bot):
#     # g_list = [913941037, 754044548]
#     # for g in g_list:
#     g = 754044548
#     members = await get_kicked_list(bot=bot, group_id=g, kicked_num=1)
#     logger.info(f"群自动清理不活跃群员初始化完成 query_start_dict : {query_start_dict}, members : {members}")

# 中转bot 消息过滤
# anderson_filter = on_message(priority=1)
# @anderson_filter.handle()
# async def _(event: GroupMessageEvent):
#     anderson_filter.block = True
#     if event.user_id == 501273515:
#         return
#     anderson_filter.block = False

# 权限过滤
permission_filter = on_command(cmd="ban", aliases={"kick", "kugm"}, priority=2)

@permission_filter.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    permission_filter.block = True
    if await(GROUP_ADMIN(bot, event) or GROUP_OWNER(bot, event)):
        await permission_filter.finish(message="机器人权限不足")
    elif event.sender.role == "member":
        await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)
        await permission_filter.finish(message="乱玩管理命令, 禁言一分钟")
    else:
        permission_filter.block = False

# 检测群是否已满, 清理不活跃用户
gm_increase = on_notice(priority=5)

@gm_increase.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):
    if await(GROUP_ADMIN(bot, event) or GROUP_OWNER(bot, event)):
        logger.info(f"群: {event.group_id} 机器人权限不足")
        return
    group_info = await bot.get_group_info(group_id=event.group_id, no_cache=True)
    if group_info["member_count"] == group_info["max_member_count"]:
        await bot.send_group_msg(message=AUTO_KICK_RULE,group_id=event.group_id)
        message_str = await kick_not_active_member(bot=bot, group_id=event.group_id, kicked_num=10)
        await gm_increase.finish(message=message_str)

# 群昵称修改提醒 group card
gc_modify = on_notice(priority=1)
@gc_modify.handle()
async def _(bot: Bot, event: NoticeEvent):
    if event.notice_type == "group_card":
        if event.user_id in (1942422015, 2412125282):
            return
        new_card = event.card_new
        if new_card[0:3].casefold() in ["id:", "id：", "id ",]:
            new_card += "(新昵称符合查询战绩/季卡条件)"
        await bot.send_group_msg(group_id=event.group_id, 
                                 message=f"{event.card_old}({event.user_id})修改群昵称为{new_card}")

# 手动命令
banuser = on_command("ban", priority=5, block=True)
kickuser = on_command("kick", priority=5 , block=True)
kugm = on_command("kugm", priority=5, permission=SUPERUSER, block=True)

@banuser.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    for seg in arg:
        if seg.type == "at":
            baned_user = seg.data.get("qq", "")
    if baned_user:
        if (await bot.get_group_member_info(group_id=event.group_id, user_id=baned_user, no_cache=True))["role"] != "member":
            await kickuser.finish(message="机器人权限不足")
        msg = arg.extract_plain_text().strip()
        ban_time = 600
        if is_number(msg) and not (int(msg) < 0 or int(msg) > 60 * 24 * 29):
            ban_time = int(msg) * 60
        await bot.set_group_ban(group_id=event.group_id, user_id=baned_user, duration=ban_time)
        logger.info(f"ban succsess group_id={event.group_id} user_id={baned_user} duration={ban_time}s")
    else:
        logger.info(f"没有@要禁的人")
        await banuser.finish(message="没有@要禁的人")

@kickuser.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    for seg in event.get_message():
        if seg.type == "at":
            kicked_user = seg.data.get("qq", "")
    if kicked_user:
        if (await bot.get_group_member_info(group_id=event.group_id, user_id=kicked_user, no_cache=True))["role"] != "member":
            await kickuser.finish(message="机器人权限不足")
        await bot.set_group_kick(group_id=event.group_id, user_id=kicked_user)
        logger.info(f"kick success group_id = {event.group_id}, user_id = {kicked_user}")
        await kickuser.finish(message=f"{kicked_user} 被我送走了")
    else:
        logger.info(f"没有@要踢的人")
        await kickuser.finish(message="没有@要踢的人")

@kugm.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    kicked_num = 10
    if is_number(msg) and not (int(msg) < 0 or int(msg) > 30):
        kicked_num = int(msg)
    result = await kick_not_active_member(bot=bot, group_id=event.group_id, kicked_num=kicked_num)
    await kugm.finish(message=result)