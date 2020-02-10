import requests
import time
import pandas as pd

from datetime import datetime

list_url = 'http://finmindapi.servebeer.com/api/datalist'
url = 'http://finmindapi.servebeer.com/api/data'

def receive_FinMindApi_JsonListData(dataset, date='', stock_id='', data_id=''):

    form_data = {"dataset": dataset}

    form_data["stock_id"] = stock_id if stock_id else None
    form_data["data_id"] = data_id if data_id else None
    form_data["date"] = date if date else None

    res = requests.post(url, verify=True, data=form_data)

    temp = res.json()
    if int(temp['status'])!=200:
        return {}
    try:
        jsonListData = temp['data']
    except BaseException:
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

if __name__ == '__main__':
    startAt = 1350230400
    endAt = 1580140800
    FundData = receive_AnueApi_JsonListData(startAt, endAt)
# min(FundData['date'])
    startDate = datetime.fromtimestamp(startAt).strftime("%Y-%m-%d")
    ustw_ExchangeRate = receive_FinMindApi_JsonListData(dataset='ExchangeRate', data_id='Taiwan', date=startDate)
    FundData['ustw_Rate'] = [ustw_ExchangeRate['InterbankRate'][ustw_ExchangeRate['date'].index(d)] if d in ustw_ExchangeRate['date'] else None for d in FundData['date']]

    def transform_TimeStamp2StringDate(timestamp):
        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        return date

    def transform_StringDate2TimeStamp(string_date):
        datetime_date = datetime.strptime(string_date, "%Y-%m-%d")
        timestamp = datetime.timestamp(datetime_date)
        return timestamp

    tmp = pd.DataFrame(FundData)
    tmp = tmp[['displayNameLocal', 'nav', 'tradeDate', 'date', 'ustw_Rate']].copy()
    tmp['q'] = tmp['date'].map(lambda x: int(transform_StringDate2TimeStamp(x)))
# min(FundData['date'])
    dataset = 'TaiwanStockPrice'
    stock_id = '2891'
    data_id = 'Taiwan'
    date = '2019-01-01'

    a = receive_FinMindApi_JsonListData(dataset, date, stock_id, data_id)
    form_data = {'dataset':'ExchangeRate','data_id':'Taiwan','date':'2019-06-01'}
    res = requests.post(url ,verify = True,data = form_data)

    temp = res.json()
    data = temp['data']

    form_data = {'dataset':'TaiwanStockPrice','stock_id':['2891'],'date':'2020-02-05'}
    res = requests.post(url, verify=True, data = form_data)
    temp = res.json()
    data = temp['data']

    print('GG')