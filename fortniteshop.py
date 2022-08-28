from nonebot.plugin import on_command
from utils.utils import scheduler, get_bot
from utils.manager import group_manager
from utils.message_builder import image
from services.log import logger
from nonebot import on_command, on_regex

__zx_plugin_name__ = "堡垒之夜每日商城"
__plugin_usage__ = """
usage：
    堡垒之夜每日商城
    指令：
        商城
""".strip()
__plugin_type__ = ("被动相关",)
__plugin_des__ = "堡垒之夜每日商城"
__plugin_cmd__ = ["商城"]
__plugin_version__ = 0.1
__plugin_author__ = "YiJiu Chow"
__plugin_task__ = {"fn":"商城"}
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商城"],
}

@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=2,
)
async def shopupshop():
    try:
        bot = get_bot()
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        for g in gl:
            if await group_manager.check_group_task_status(g, 'fn'):
                result = image("https://cdn.dingpanbao.cn/blzy/shop.png")
                await bot.send_group_msg(group_id=g, message=result) 
    except:
        logger.error("商城错误")

shopshop = on_command("商城", priority=5, block=True)    
@shopshop.handle()
async def _():
    await shopshop.finish(message=image("https://cdn.dingpanbao.cn/blzy/shop.png"))
