import os
import time
import pandas as pd

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Invest.Tool.common import calculate_2stringDate_Datenbr, get_Current_Date
from Invest.Reports import config

driver = webdriver.Chrome(config.CHROMEDRIVER_PATH)
driver.get('https://www.anuefund.com/Login.aspx')

elem = driver.find_elements_by_id('ContentPlaceHolder1_txtCustID')
elem[0].send_keys(config.ACCOUNT)

password = driver.find_elements_by_id('ContentPlaceHolder1_txtPWD')
password[0].send_keys(config.PASSWORD)
elem[0].send_keys(Keys.RETURN)

def prase_Html(stringHtml):
    tree = etree.HTML(stringHtml)
    tables = tree.xpath('//table[@class="table-gold-th"]')
    assert len(tables)!=0, '請登入網站'
    table = tables[0]

    tbody = []
    for row in table.xpath("tbody/tr"):
        tds = row.xpath("td")
        
        data = []
        for i, td in enumerate(tds):
            if i == 1: # 基金代碼
                ele = td.xpath("a")[0].text
                data.append(ele)
            elif i in [2, 3, 4]: # 幣別, [總投資成本, 持有單位數], [淨值, 淨值日期] 
                ele = td.text
                data.append(ele)

                ele2 = td.xpath("br")[0].tail
                data.append(ele2)
            elif i == 6: # [約當市值, 損益]
                ele = td.text
                data.append(ele)

                ele2 = td.xpath("span")[0].text
                data.append(ele2)
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

time.sleep(10)
stringHtml = driver.page_source
tbody = prase_Html(stringHtml)
listData = clean_RawData(tbody)

columns = ['基金代碼', '基金名稱', '交易幣別', '計價幣別', '總投資成本', '持有單位數', 
    '淨值', '淨值日期', '參考匯率', '約當市值', '損益', '已配息金額', '(不含息)', '(已含息)']

ret = pd.DataFrame(listData, columns=columns)
ret['(已含息)'] = ret['(已含息)'].map(lambda x: float(x.replace('%', '')))
ret['(不含息)'] = ret['(不含息)'].map(lambda x: float(x.replace('%', '')))
ret['總投資成本'] = ret['總投資成本'].map(lambda x: float(x.replace(',', '')))
ret[['持有單位數', '參考匯率']] = ret[['持有單位數', '參考匯率']].astype(float) 

ret['投資起始日期'] = ret['基金代碼'].map(config.ST_TRADE_DATE_MAPPING)
ret['投資時間'] = ret['投資起始日期'].map(lambda x: calculate_2stringDate_Datenbr(x, get_Current_Date())/365)
ret['含息年化報酬'] = ret.apply(lambda x: round( ( ((1+(x['(已含息)']/100)) ** (1/x['投資時間'])) - 1), 3), axis=1)
ret['單位平均價格'] = ret['總投資成本'] / ret['持有單位數'] / ret['參考匯率']

report_name = 'AnueFundReport_{}.csv'.format(get_Current_Date())
save_path = os.path.join('./Invest/Data/Report/', report_name)
ret.to_csv(save_path, index=False, encoding='utf_8_sig')
driver.close()
