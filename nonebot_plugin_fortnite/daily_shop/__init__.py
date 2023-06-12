from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from utils.utils import scheduler, get_bot
from utils.manager import group_manager
from utils.message_builder import image
from services.log import logger
from configs.path_config import IMAGE_PATH

import os, httpx, asyncio

__zx_plugin_name__ = "商城"
__plugin_usage__ = """
usage：
    堡垒之夜每日商城
    指令：
        商城
""".strip()
__plugin_type__ = ("堡批专属",)
__plugin_cmd__ = ["商城"]
__plugin_des__ = "堡垒之夜每日商城"
__plugin_task__ = {"fn":"堡垒之夜商城推送"}


shop_path = "/home/ubuntu/datou/zhenxun_bot/resources/image/shop.png"

@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=3,
)
async def shopupshop():
    while True:
        try:
            result = update_dailyshop()
            break
        except Exception as e:
            logger.error(f"商城更新错误 {e}")
            # 网络错误, 重新更新
            await asyncio.sleep(10)
            continue
    bot = get_bot()
    gl = await bot.get_group_list()
    gl = [g["group_id"] for g in gl]
    for g in gl:
        if group_manager.check_group_task_status(g, 'fn'):
            await bot.send_group_msg(group_id=g, message=result) 


shopshop = on_command("商城", priority=5, block=True)    
@shopshop.handle()
async def _():
    await shopshop.finish(message=image(file="shop.png"))


updateshop = on_command("更新商城", priority=5, block=True, permission=SUPERUSER)
@updateshop.handle()
async def _():
    result = update_dailyshop()
    await updateshop.finish(message="手动更新商城成功" + result)

def update_dailyshop():
    resp = httpx.get(url= "https://cdn.dingpanbao.cn/blzy/shop.png")
    with open(shop_path, "wb") as f:
        f.write(resp.content)
    result = image(file="shop.png")
    return result