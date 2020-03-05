import requests
import pandas as pd

from lxml import etree
from io import BytesIO

from Invest.Tool.common import calculate_Datenbr, get_Current_Date
from Invest.Reports import config


def prase_Html(response):
    tree = etree.parse(BytesIO(response.content), etree.HTMLParser())
    tables = tree.xpath('//table[@class="table-gold-th"]')
    assert len(tables)!=0, '請登入網站'
    table = tables[0]

    tbody = []
    for row in table.xpath("tbody/tr"):
        tds = row.xpath("td")
        
        data = []
        for i, td in enumerate(tds):
            if i == 1:
                ele = td.xpath("a")[0].text
                data.append(ele)
            elif i in [2, 3, 4]:
                ele = td.text
                data.append(ele)

                ele2 = td.xpath("br")[0].tail
                data.append(ele2)
            elif i == 6:
                ele = td.text
                data.append(ele)

                ele2 = td.xpath("span")[0].text
                data.append(ele)
            elif i == 7:
                ele = td.text
                data.append(ele)
            elif i == 8 or i == 9:
                for span in td.xpath("span"):
                    ele = span.text
                    data.append(ele)
            else:
                ele = td.text
                data.append(ele)

        tbody.append(data)
    return tbody

def clean_RawData(tbody):
    new_tbody = []
    for row in tbody:
        new_row =  [ele.strip('\r\n').strip() for ele in row]
        new_tbody.append(new_row)
    return new_tbody

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "rate.bot.com.tw",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    
    # 把Cookie塞進来
    'Cookie': config.COOKIE
}

session = requests.Session()
response = session.get('https://www.anuefund.com/EC/OverView.aspx', headers=header)

tbody = prase_Html(response)
listData = clean_RawData(tbody)

columns = ['基金代碼', '基金名稱', '交易幣別', '計價幣別', '總投資成本', '持有單位數', 
    '淨值', '淨值日期', '參考匯率', '約當市值', '損益', '已配息金額', '(不含息)', '(已含息)']

ret = pd.DataFrame(listData, columns=columns)
ret['(已含息)'] = ret['(已含息)'].map(lambda x: float(x.replace('%', '')))
ret['(不含息)'] = ret['(不含息)'].map(lambda x: float(x.replace('%', '')))

ret['投資起始日期'] = ret['基金代碼'].map(config.ST_TRADE_DATE_MAPPING)
ret['投資時間'] = ret['投資起始日期'].map(lambda x: calculate_Datenbr(x, get_Current_Date())/365)
ret['含息年化報酬'] = ret.apply(lambda x: round(float(((1+(x['(已含息)']/100))**(1/x['投資時間'])) - 1), 3), axis=1)



print(response.text)



