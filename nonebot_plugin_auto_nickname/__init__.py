import time, asyncio
from random import choice
from nonebot.adapters.onebot.v11 import Bot

from services.log import logger
from utils.utils import scheduler, get_bot

__zx_plugin_name__ = "时间群昵称"
__plugin_version__ = 0.1
__plugin_author__ = "YiJiuChow"


# lz_list = ["绿头鸡", "鸡脖哥", "鸡脖王", "鸡脖哥哥"]
# gl = [754044548, 208248400] # [669026253,, 782270111, 1080197262, 1149277515, 913941037] # 

gl: list

@scheduler.scheduled_job("interval", minutes=1)
async def _():
    bot = get_bot()
    if not gl:
        gl = [g["group_id"] for g in bot.get_group_list()]
    if bot:
        timestr = time.strftime("%a %b %d %H:%M %Y CST", time.localtime())
        for g in gl:
            await bot.set_group_card(group_id=g, user_id=bot.self_id, card=f"大头 {timestr}")
            await asyncio.sleep(1)
        # await bot.set_group_card(group_id=774331907, user_id=1626303708, card=choice(lz_list)) 