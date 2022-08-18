import httpx
from bs4 import BeautifulSoup
import re

epic_nickname = "红桃QAQ"
url = f"https://api.fortnitetracker.com/v1/profile/kbm/{epic_nickname}"

headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}

def getTags(html):
    reg = r'<div class="trn-session__details-stat__name">([\s\S]+?)</div>'
    pattern= re.compile(reg)
    tags= re.findall(pattern, html)
    return tags


fhtml = httpx.get(url, headers=headers)
soup=BeautifulSoup(fhtml.text,'lxml')
print(soup.find_all(name='div',attrs={"class":"trn-session__details-stat__value"}))
##data = soup.select('#profile > div.trn-scont > div.trn-scont__content > div > div:nth-child(3) > div:nth-child(1) > div.trn-session__details > div:nth-child(2)')
with open("text.txt","w") as file:
    file.write(fhtml.text)


# print(data)
# for item in data:
#     result={
#         'title':item.get_text,
#         'name':item.get_attribute_list,
#         'value':item.get('trn-session__details-stat__value'),
#         ##'text':re.findall('\d+',item.get('href'))
#     }
#     print(result)

