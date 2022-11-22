from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg

from services.log import logger
from utils.utils import scheduler, get_bot
from myplugins.myutils.mystr import MyStr

import datetime, time



__zx_plugin_name__ = "时间群昵称"
__plugin_version__ = 0.1
__plugin_author__ = "YiJiuChow"


todo_dict: dict = {}

todo = on_command("todo", priority=5, permission=SUPERUSER, block=True)
@todo.handle()
async def _(event: PrivateMessageEvent, args: Message = CommandArg()):
    job_str = args.extract_plain_text().split(' ')
    todo_dict[job_str[0]] = job_str[1]
    lt = time.localtime()
    scheduler.add_job(
        todo_aps, "date", 
        run_date = datetime.datetime(lt.tm_year, lt.tm_mon, lt.tm_mday, int(job_str[0][0:2]), int(job_str[0][2:4]), 0),
        id = job_str[0], args = [job_str[0]])
    await todo.finish(message=MyStr()
            .append_line("TODO JOB ADD SUCCESS")
            .append_line("  You're going to do:")
            .append_line(f"  -- {job_str[0][0:2]}:{job_str[0][2:4]} {job_str[1]}")
            .append_line("  I'll remind you then.")
            .append("END")
        )

todo_list = on_command("todolist", priority=5, permission=SUPERUSER, block=True)
@todo_list.handle()
async def _():
    td_list = MyStr()
    for k, v in todo_dict.items():
        td_list.append_line(f"  {k[0:2]}:{k[2:4]} {v}")
    await todo_list.finish(message=
        MyStr()
            .append_line("TODO JOB LIST")
            .append_line("  You're going to do:")
            .append_line(td_list.value)
            .append_line("  I'll remind you then.")
            .append("END"))

async def todo_aps(job_id: str):
    bot = get_bot()
    await bot.send_private_msg(user_id='1942422015', 
        message=MyStr()
            .append_line("TODO JOB")
            .append_line("  You should be right now:")
            .append_line(  -- todo_dict[job_id])
            .append_line("  Right now. Right now.")
            .append("END")
        )
    del todo_dict[job_id]
    

    