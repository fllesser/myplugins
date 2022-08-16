from concurrent.futures import thread
from time import sleep
from nonebot import on_request
from nonebot.typing import T_State
from nonebot.params import State, ArgStr
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupRequestEvent,
    GroupMessageEvent,
    MessageSegment
)
import random
from services.log import logger


__zx_plugin_name__ = "入群验证"
__plugin_version__ = 0.1
__plugin_author__ = "YiJiuChow"


group_req = on_request(state = State())
@group_req.handle()
async def _(
    bot: Bot,
    event: GroupRequestEvent,
    state
):
    try:
        await sleep(1.5)
        await bot.set_group_add_request(flag=event.flag, approve=True)
        await sleep(1.5)
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        state["group_verify"] = x + y
        await bot.send_group_msg(group_id=event.group_id, message= f"{MessageSegment.at(event.user_id)}\n请计算并发送{x}+{y}的结果\n回答错误或超过30秒未作答将踢出群聊")
    except Exception as e:
        logger.error(f"入群验证 错误信息{e}")
    
@group_req.got("group_verify")
async def _(
    bot: Bot, 
    event: GroupMessageEvent,
    state,
    target_text: str = ArgStr("group_verify")
):
    if target_text == state["group_verify"]:
        await group_req.finish("恭喜你完成了入群验证, 汉化包等问题请前往公告", at_sender=True)
    else:
        await bot.set_group_kick(user_id=event.user_id, group_id=event.group_id)



        