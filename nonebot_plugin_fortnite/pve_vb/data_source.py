import httpx
import time

from bs4 import BeautifulSoup
from PIL import Image, ImageFont
from io import BytesIO

from configs.path_config import IMAGE_PATH, FONT_PATH
from utils.message_builder import image
from services.log import logger
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH


async def update_daily_vb() -> str:
    url = "https://freethevbucks.com/timed-missions/"
    async with httpx.AsyncClient as client:
        free_resp = await client.get(url)
        ele_resp = await client.get("https://img.icons8.com/office/30/000000/lightning-bolt.png")
    soup = BeautifulSoup(free_resp.content, "lxml")
    # 电力图标
    ele_img = Image.open(BytesIO(ele_resp.content))
    ele_img = ele_img.resize((20, 20), Image.LANCZOS)
    # TODO 准备加一个vb图标
    # vb_icon = Image.open(BytesIO(httpx.get().content))
    # vb图
    img = BuildImage(w=256, h=200, font_size=15,
                    color=(36, 44, 68), font="gorga.otf")
    # 起始纵坐标
    Y = 30
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    await img.atext(pos=(0, 170), text=timestr, center_type="by_width", fill=(255, 255, 255))
    for item in soup.find_all("p"):
        if item.span is not None and item.span.b is not None:
            storm_src = item.img.get("src")  # 风暴图标链接
            async with httpx.AsyncClient as client:
                resp = await client.get(storm_src)
            storm_img = Image.open(BytesIO(storm_img.content))
            await img.apaste(img=storm_img, pos=(40, Y), alpha=True)  # 风暴图标
            # 电力
            await img.atext(text=item.b.string, pos=(70, Y-3), fill=(255, 255, 255))
            await img.apaste(img=ele_img, pos=(100, Y+1), alpha=True)  # 电力图标
            await img.atext(pos=(130, Y-3), text=item.span.text, fill=(255, 255, 255))
            Y += 30
    if Y == 30:
        img.font = ImageFont.truetype(str(FONT_PATH / "HWXingKai.ttf"), 30)
        await img.atext(pos=(0, 80), text="今天没有vb图捏", center_type="by_width", fill=(255, 255, 255))
    img.save(IMAGE_PATH / "fn_stw.png")
    return "fn_stw.png"