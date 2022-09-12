import random, os, asyncio

from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER

from services.log import logger
from utils.utils import scheduler, get_bot

__zx_plugin_name__ = "今日校园自动签到 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "YiJiuChow"

# 默认定时任务
@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=10,
    id='today_school'
)
async def ts(): # 签到函数
    bot = get_bot()
    ts_command = "python3 auto-cpdaily/index.py"
    try:
        if os.path.exists("success.info"):
            os.remove("success.info")
        os.popen(ts_command)
        logger.info(f"今日校园 {ts_command} 开始执行")
        await asyncio.sleep(80)
        with open("success.info", 'r') as f:
            str = f.read()
        logger.info(f"今日校园自动签到任务执行完毕 {str}")
    except Exception as e:
        logger.error(f"今日校园错误 {e}")
    if bot:
        #superusers_set = bot.config.superusers
        #for superuser in superusers_set:
        await bot.send_group_msg(group_id=774331907, message=Message(f"今日校园签到状态: {str}"))

@scheduler.scheduled_job(
    "cron",
    hour=3,
    minute=5,
    id='add_today_school_job'
) 
async def _():
    try:
        scheduler.remove_job("today_school")
        interval_minutes = random.randint(1, 59)
        interval_hours = random.randint(7, 9)
        scheduler.add_job(ts, "cron", hour=interval_hours, minute=interval_minutes, id='today_school')
        logger.info(f"添加今日校园定时任务 SUCCESS {interval_hours}时{interval_minutes}分")
    except Exception as e:
        logger.error(f"添加今日校园任务错误 {e}")

# 今日校园手动签到命令
cp_daily = on_command("tsc", priority=5, permission=SUPERUSER, block=True)

@cp_daily.handle()
async def _(event: PrivateMessageEvent):
    await ts()


# # 今日校园手动添加任务命令
# add_cp_daily = on_command("addtsc", priority=5, permission=SUPERUSER, block=True)

# @add_cp_daily.handle()
# async def _(event: PrivateMessageEvent):
#     scheduler.remove_job("today_school")
#     interval_minutes = random.randint(1, 59)
#     interval_hours = random.randint(7, 9)
#     scheduler.add_job(ts, "cron", hour=interval_hours, minute=interval_minutes, id='today_school')
#     logger.info(f"手动添加今日校园定时任务 SUCCESS {interval_hours}时{interval_minutes}分")
#     await add_cp_daily.finish(message=f"添加今日校园签到任务 {interval_hours}时{interval_minutes}分")

        