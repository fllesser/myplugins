from nonebot import on_command
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.params import CommandArg, ArgStr
from .data import text_to_emoji

__zx_plugin_name__ = "抽象化语句"
__plugin_des__ = "抽象化"
__plugin_type__ = ("功能",)
__plugin_usage__ = """
usage:
    抽象化语句
    指令:
        abs xxx
        抽象 xxx

""".strip()

__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["abs"],
}


abstract = on_command("abs", aliases={"抽象", "抽象化"}, priority=5, block=True)

@abstract.handle()
async def _(state: T_State = State(), arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        state["abstract"] = arg.extract_plain_text().strip()

@abstract.got("abstract", prompt="你要抽象什么？")
async def _(bot: Bot, event: Event, target_text: str = ArgStr("abstract")):
    abstract_responses = text_to_emoji(target_text)
    if abstract_responses:
        logger.info("抽象成功！")
        await abstract.send(abstract_responses)
    else:
        logger.error("抽象失败~")
        await abstract.send("抽象异常了~一定是程序出了点问题！")
