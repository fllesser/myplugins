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

async def update_daily_vb():
    url = "https://freethevbucks.com/timed-missions/"
    html_content = httpx.get(url).content
    soup = BeautifulSoup(html_content, "lxml")
    # vb图
    img = BuildImage(w=256, h=200, font_size=15, color=(36, 44, 68), font="gorga.otf")
    Y = 30
    # 电力图标
    ele_img = Image.open(BytesIO(httpx.get("https://img.icons8.com/office/30/000000/lightning-bolt.png").content))
    ele_img = ele_img.resize((20, 20), Image.LANCZOS)
    # 当前时间
    timestr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    await img.atext(pos=(0, 170),text=timestr, center_type="by_width", fill=(255, 255, 255))
    for item in soup.find_all("p"):
        if item.span is not None:
            if item.span.b is not None:
                storm_src = item.img.get("src") # 风暴图标链接
                storm_img = httpx.get(storm_src).content
                storm_img = Image.open(BytesIO(storm_img))
                await img.apaste(img=storm_img, pos=(40, Y), alpha=True) # 风暴图标
                await img.atext(text=item.b.string, pos=(70, Y-3), fill=(255, 255, 255)) # 电力
                await img.apaste(img=ele_img, pos=(100, Y+1), alpha=True) # 电力图标
                await img.atext(pos=(130, Y-3), text= item.span.text, fill=(255, 255, 255))
                Y += 30
    if Y == 30:
        img.font = ImageFont.truetype(str(FONT_PATH / "HWXingKai.ttf"), 30)
        await img.atext(text="今天没有vb图捏", pos=(0, 80), center_type="by_width", fill=(255, 255, 255))
    img.save(IMAGE_PATH / "fn_stw.png")
    