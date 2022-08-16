import os
import re
import string
from bs4 import SoupStrainer
from fortnite_api import TimeWindow,GameLanguage,StatsImageType
import fortnite_api
import json
import httpx
from PIL import Image, ImageFont, ImageDraw
from numpy import size, unicode_
from pyparsing import unicode_string
import requests
from io import BytesIO
import matplotlib.font_manager as fm
import base64

def getrank():
    api = fortnite_api.FortniteAPI(api_key = "f3f4e682-346e-45b1-8323-fe77aaea2a68",run_async = False)
    nickname = "Jarid Harris"
    nickname = "爱吃菠萝包的猫"
    # nickname = "ж老冰棍ж"
    # nickname = "阿姨好阿姨香阿姨是深夜里的一缕光"
    try:
        playerstats = api.stats.fetch_by_name(nickname,image=StatsImageType.ALL)
        url = playerstats.image_url
    
        ##fm.rcParams['font.sans-serif'] = ['Simhei']
        ##ttfont = ImageFont.truetype(fm.findfont(fm.FontProperties(family='serif')), 28, encoding="utf-8")
        if re.search(r'[\u2E80-\u9FFF]', nickname, flags=0):
            ttfont = ImageFont.truetype("simhei.ttf", 30)
            response = httpx.get(url)
            im = Image.open(BytesIO(response.content))
            #print(im.format, im.size, im.mode)

            draw = ImageDraw.Draw(im) #修改图片
            X = 225 - len(nickname) * 15
            if X < 0:
                X = 0
            xy=(30, 90, 420, 230)
            draw.rectangle(xy=xy, fill="#012e57")
            draw.text((X,150), f'{nickname}', fill = "#fafafa", font=ttfont)
            im.show()
        else:
            response = httpx.get(url)
            im = Image.open(BytesIO(response.content))
            im.show()
    except Exception as e:
        print(e)

def image_to_base64(image: Image.Image, fmt='png') -> str:
    output_buffer = BytesIO()
    image.save(output_buffer, format=fmt)
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return f'data:image/{fmt};base64,' + base64_str

getrank()

