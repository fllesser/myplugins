from nonebot import require
import datetime, random, time
from nonebot import get_bot, logger


scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job(
    "interval",
    minutes=1
)
async def _():
    try:
        bot = get_bot()
        gl = [913941037, 754044548, 782270111, 774331907, 1080197262, 299909569, 768887710]
        now = datetime.datetime.now()
        df = datetime.datetime.strptime('2023-06-22 00:00:00', '%Y-%m-%d %H:%M:%S')
        em = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        delta = (df - now) + em
        for g in gl:
            await bot.set_group_card(
                group_id=g,
                user_id=bot.self_id,
                card=f"毕(shi)业倒计时[GC]:{(df - now).days}天{delta.hour}时{delta.minute}分{random.randint(1,60)}秒")
    except Exception as e:
        logger.error(f"super_nickname error: {e}")

@scheduler.scheduled_job(
    "cron",
    hour=6,
    minute=0,
)
async def _():
    try:
        bot = get_bot()
        timestr = time.strftime("%a %b %d %Y CST", time.localtime())
        await bot.call_api("set_qq_profile", nickname=f"Oswald Kan {timestr}")
    except Exception as e:
        logger.error(f"set_qq_profile error: {e}")
