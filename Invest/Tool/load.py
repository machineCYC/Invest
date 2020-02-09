import requests
import time
import pandas as pd

from datetime import datetime

list_url = 'http://finmindapi.servebeer.com/api/datalist'
url = 'http://finmindapi.servebeer.com/api/data'

def receive_FinMindApi_JsonListData(datadet, stock_id, date):
    form_data = {'dataset':datadet,'stock_id':stock_id,'date':date}
    res = requests.post(url, verify=True, data = form_data)

    temp = res.json()
    if int(temp['status'])==200:
        jsonListData = temp['data']
    else:
        jsonListData = {}
    return jsonListData

def receive_AnueApi_JsonListData(startAt, endAt):
    url = 'https://api.cnyes.com/api/v1/fund/B20%2C073/nav?startAt={}&endAt={}'.format(startAt, endAt)
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'api.cnyes.com',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    time.sleep(5)
    res = requests.get(url, verify=True, headers=header)
    tem = res.json()
    if tem['statusCode'] != 200:
        return {}
    try:
        jsonListData = tem['items']
    except BaseException:
        return {}
    colname = list(tem['items'].keys())
    jsonListData['date'] = list(map(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d"), jsonListData['tradeDate']))
    return jsonListData

startAt = 1350230400
endAt = 1580140800
data = receive_AnueApi_JsonListData(startAt, endAt)

# form_data = {'dataset':'TaiwanStockPrice','stock_id':['2891'],'date':'2020-02-05'}
# res = requests.post(url, verify=True, data = form_data)
# temp = res.json()
# data = temp['data']

print('GG')