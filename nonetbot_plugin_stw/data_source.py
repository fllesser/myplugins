import httpx

from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from services.log import logger
from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH

# async def get_vbmap() -> Optional[MessageSegment]:
#     url = "https://freethevbucks.com/timed-missions/"
#     # url = "https://baidu.com"
#     try:
#         browser = await get_browser()
#         context = await browser.new_context()
#         page = await context.new_page()
#         await page.goto(
#             url=url,
#             timeout=30000,
#         )
#         # await page.set_viewport_size(
#         #     {"width": 1200, "height": 800, "timeout": 10000 * 20}
#         # )
#         # await page.wait_for_selector(".infonotice")
#         # card = page.locator(".main-title")
#         # await card.wait_for()
#         await page.screenshot(
#             path=IMAGE_PATH / "fn_stw.jpg",
#         )
#     except Exception as e:
#         logger.error(e)
#     finally:
#         await context.close()
#         await page.close()
#     return image("fn_stw.jpg")

async def get_vbmap_byhttpx():
    url = "https://freethevbucks.com/timed-missions/"
    html_content = httpx.get(url).content
    soup = BeautifulSoup(html_content, "lxml")
    # img = Image.new('RGB', (256, 256), (36, 44, 68))
    # 合集图
    img = BuildImage(w=256, h=200, font_size=15, color=(36, 44, 68), font="gorga.otf")
    Y = 40
    # 电力图标
    ele_img = httpx.get("https://img.icons8.com/office/30/000000/lightning-bolt.png").content
    ele_img = Image.open(BytesIO(ele_img))
    ele_img = ele_img.resize((20, 20), Image.LANCZOS)
    for item in soup.find_all("p"):
        if item.span is not None:
            if item.span.b is not None:
                storm_src = item.img.get("src") # 风暴图类型
                storm_img = httpx.get(storm_src).content
                storm_img = Image.open(BytesIO(storm_img))
                await img.apaste( # 异步改为apaste
                    img=storm_img,
                    pos=(40, Y),
                    alpha=True
                )
                await img.atext( # 异步改为atext
                    pos=(70, Y-3),
                    text= item.b.string, # 电力
                    fill=(255, 255, 255)
                )
                await img.apaste( # 异步改为apaste
                    img=ele_img,
                    pos=(100, Y+1),
                    alpha=True
                )
                await img.atext( # 异步改为atext
                    pos=(130, Y-3),
                    text= item.span.text, # vb
                    fill=(255, 255, 255)
                )
                Y += 30
    img.save(IMAGE_PATH / "fn_stw.png")
    