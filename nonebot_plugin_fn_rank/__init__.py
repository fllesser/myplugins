from nonebot.params import T_State,State, CommandArg
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message

from utils.message_builder import image
from utils.image_utils import pic2b64
from configs.path_config import FONT_PATH
from services.log import logger

from fortnite_api import StatsImageType, FortniteAPI
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import httpx, re

__zx_plugin_name__ = "堡垒之夜战绩查询"
__plugin_usage__ = """
usage：
    堡垒之夜战绩查询
    指令：
        战绩
""".strip()
__plugin_des__ = "堡垒之夜战绩查询"
__plugin_cmd__ = ["战绩"]
__plugin_version__ = 0.1
__plugin_author__ = "YiJiu Chow"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["战绩查询"],
}


api = FortniteAPI(api_key = "f3f4e682-346e-45b1-8323-fe77aaea2a68",run_async = True)

fortniterank = on_command("战绩", block=True)
@fortniterank.handle()
async def _(bot: Bot, event: Event, state:T_State=State(), args: Message = CommandArg()):
    nickname = args.extract_plain_text()
    if nickname is None or nickname == '':
        await fortniterank.finish(message="ID都没, 查个鬼的战绩蛮")
    try:
        playerstats = await api.stats.fetch_by_name(nickname,image=StatsImageType.ALL)
        url = playerstats.image_url
        result = None
        # 匹配带中文昵称
        if re.search(r'[\u2E80-\u9FFF]', nickname, flags=0):
            response = httpx.get(url)
            im = Image.open(BytesIO(response.content))
            draw = ImageDraw.Draw(im) 
            # 覆盖
            draw.rectangle(xy=(30, 90, 420, 230), fill="#012e57")
            # 填充昵称
            cn_len = (len(nickname.encode("utf-8")) - len(nickname.encode("GBK")))
            nickname_len = (len(nickname) - cn_len + 0.0) / 2 + cn_len
            font_size = 30
            X = max((225 - nickname_len * font_size / 2), 0)
            font = "yz.ttf"
            ttfont = ImageFont.truetype(str(FONT_PATH / font), font_size)
            draw.text((X, 150), f'{nickname}', fill = "#fafafa", font=ttfont)
            result = im
    except Exception as e:
        await fortniterank.finish(message=str(e))
    logger.info("战绩查询成功")
    if result is not None:
        await fortniterank.finish(message=image(b64=pic2b64(result)))
    else:
        await fortniterank.finish(message=image(url))