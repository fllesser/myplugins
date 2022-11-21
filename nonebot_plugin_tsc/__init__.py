import random, os, asyncio

from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER

from services.log import logger
from utils.utils import scheduler, get_bot

__zx_plugin_name__ = "今日校园自动签到 [Hidden]"
__plugin_version__ = 0.1
__plugin_author__ = "YiJiuChow"

TS_ID = "today_school"
FILE_NAME = "success.info"

# 默认定时任务
@scheduler.scheduled_job("cron", hour=3, minute=10, id=TS_ID)
async def ts(): # 签到函数
    bot = get_bot()
    ts_command = "python3 auto-cpdaily/index.py"
    try:
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        os.popen(ts_command)
        logger.info(f"今日校园 {ts_command} 开始执行")
        await asyncio.sleep(80)
        with open(FILE_NAME, 'r') as f:
            str = f.read()
        logger.info(f"今日校园自动签到任务执行完毕 {str}")
    except Exception as e:
        logger.error(f"今日校园错误 {e}")
    if bot:
        #superusers_set = bot.config.superusers
        #for superuser in superusers_set:
        await bot.send_group_msg(group_id=774331907, message=Message(f"今日校园签到状态: {str}"))

@scheduler.scheduled_job("cron", hour=3, minute=5) 
async def _():
    scheduler.remove_job(TS_ID)
    interval_minutes = random.randint(1, 59)
    interval_hours = random.randint(7, 9)
    scheduler.add_job(ts, "cron", hour=interval_hours, minute=interval_minutes, id=TS_ID)
    logger.info(f"添加今日校园定时任务 SUCCESS {interval_hours}时{interval_minutes}分")


# 今日校园手动签到命令
cp_daily = on_command("tsc", priority=5, permission=SUPERUSER, block=True)
@cp_daily.handle()
async def _(event: PrivateMessageEvent):
    await ts()
        