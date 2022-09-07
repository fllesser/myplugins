from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from utils.utils import scheduler, get_bot
from services.log import logger
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from utils.manager import group_manager

from .data_source import update_daily_vb

__zx_plugin_name__ = "STW(PVE)"
__plugin_usage__ = """
usage：
    堡垒之夜PVE
    指令：
        pve
""".strip()
__plugin_author__ = "YiJiu Chow"
__plugin_task__ = {"pve":"堡垒之夜PVE推送"}
__plugin_settings__ = {
    "level": 5,
    "default_status": False,
    "limit_superuser": False,
    "cmd": ["pve"],
}

pve = on_command("pve", aliases={"vb图", "VB图", "V币图", "v币图"}, priority=5, block=True)
@pve.handle()
async def _():
    await pve.finish(message=image(IMAGE_PATH / "fn_stw.png"))

update_pve = on_command("u pve", priority=5, block=True, permission=SUPERUSER)
@update_pve.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await update_daily_vb()
    await bot.send_group_msg(group_id=event.group_id,message="手动更新 STW(PVE) vb图成功")

@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=1,
)
async def _():
    try:
        await update_daily_vb()
        bot = get_bot()
        gl = await bot.get_group_list()
        gl = [g["group_id"] for g in gl]
        for g in gl:
            if await group_manager.check_group_task_status(g, 'pve'):
                await bot.send_group_msg(group_id=g, message=image(IMAGE_PATH / "fn_stw.png")) 
    except Exception as e:
        logger.error("PVE vb图更新错误 {e}")
