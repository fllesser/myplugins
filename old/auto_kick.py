import asyncio
import time
from utils.utils import scheduler, is_number
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
)
from nonebot import on_command
from nonebot.params import CommandArg
from services.log import logger

__zx_plugin_name__ = "踢除不活跃用户 [Admin]"
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


kugm = on_command("kugm", priority=5, block=True)

@kugm.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    kicked_num = 10
    if is_number(msg) and not (int(msg) < 0 or int(msg) > 30):
        kicked_num = int(msg)
    now_time = int(time.time())
    # 群员列表
    gm_list = await bot.get_group_member_list(group_id=event.group_id)
    # 待踢列表
    member_list = None
    member_list = []
    # 待踢成员计数
    kicked_count = 0
    for member in gm_list:
        if (now_time - int(member["last_sent_time"]) > 7777777) and int(member["level"]) < 50:
            member_list.append(member["user_id"])
            kicked_count += 1
        if kicked_count == kicked_num:
            gm_list = None
            break
    for user_qq in member_list:
        await bot.set_group_kick(group_id=event.group_id, user_id=user_qq)
        logger.info(f"group:{event.group_id} user_id={user_qq} 已踢")
        await asyncio.sleep(1)
    await kugm.finish(message=f"{member_list} 被我通通送走了")





