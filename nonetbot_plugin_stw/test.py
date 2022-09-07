from turtle import color
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time


from utils import BuildImage
# from utils.message_builder import text

url = "https://freethevbucks.com/timed-missions/"
html_content = requests.get(url).content
soup = BeautifulSoup(html_content, "lxml")
# img = Image.new('RGB', (256, 256), (36, 44, 68))
# 合集图
img = BuildImage(w=256, h=200, font_size=15, color=(36, 44, 68), font="gorga.otf")
Y = 20
# 电力图标
ele_img = Image.open(BytesIO(requests.get("https://img.icons8.com/office/30/000000/lightning-bolt.png").content))
ele_img = ele_img.resize((20, 20), Image.LANCZOS)
timestr = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
img.text(pos=(0, 170),text=timestr, center_type="by_width", fill=(255, 255, 255))
for item in soup.find_all("p"):
    if item.span is not None:
        if item.span.b is not None:
            storm_src = item.img.get("src") # 风暴图类型
            
            img.paste( # 异步改为apaste
                img=Image.open(BytesIO(requests.get(storm_src).content)),
                pos=(40, Y),
                alpha=True
            )
            img.text( # 异步改为atext
                pos=(70, Y-3),
                text= item.b.string, # 电力
                fill=(255, 255, 255)
            )
            img.paste( # 异步改为apaste
                img=ele_img,
                pos=(100, Y+1),
                alpha=True
            )
            img.text( # 异步改为atext
                pos=(130, Y-3),
                text= item.span.text, # vb
                fill=(255, 255, 255)
            )
            Y += 30
if Y == 20:
    img.font.size=30
    img.text(text="今天没有vb图捏",pos=(0, 100) ,center_type="center")
img.save("test.png")
