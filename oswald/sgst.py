from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
)
from nonebot import on_command
from nonebot.log import logger
from nonebot.params import CommandArg
from typing import List, Union
try:
    import ujson as json
except ModuleNotFoundError:
    import json


def get_message_at(data: Union[str, Message]) -> List[int]:
    """
    说明：
        获取消息中所有的 at 对象的 qq
    参数：
        :param data: event.json()
    """
    qq_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                qq_list.append(int(msg["data"]["qq"]))
    else:
        for seg in data:
            if seg.type == "at":
                qq_list.append(seg.data["qq"])
    return qq_list

sgst = on_command("sgst", aliases={"设置专属头衔"})

@sgst.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    # sted_user = get_message_at(event.json())[0]
    msg = arg.extract_plain_text().strip()
    if msg:
        msg = msg.split()
        try:
            msg = msg[0]
            if not (len(msg) < 0 or len(msg) > 6):
                if not "群主" in msg: 
                    await bot.set_group_special_title(group_id = event.group_id, user_id = event.user_id, special_title = msg)
                    logger.info(f"ban_user group_id={event.group_id} user_id={event.user_id} special_title = {msg}")
            else:
                await sgst.send(message=f"Bot代发:群头衔最多6位, 字母也算一位")
        except Exception as e:
            logger.error(f"set_group_special_title error: {e}")