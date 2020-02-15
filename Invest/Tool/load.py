import requests
import time
import pandas as pd

# from datetime import datetime
from Invest.Tool.common import transform_TimeStamp2StringDate

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

    for c in [ 'nav', 'tradeDate', 'change', 'changePercent']:
        jsonListData[c] = jsonListData[c][::-1]
    return jsonListData

if __name__ == '__main__':
    startAt = 1350230400
    endAt = 1580140800
# min(FundData['date'])

    from Invest.Tool.common import transform_TimeStamp2StringDate
    # import datetime as dt
    startDate = transform_TimeStamp2StringDate(startAt)
    FundData = receive_AnueApi_JsonListData(startAt, endAt)
    ustw_ExchangeRate = receive_FinMindApi_JsonListData(dataset='ExchangeRate', data_id='Taiwan', date=startDate)

    FundData_df = pd.DataFrame(FundData)
    ustw_ExchangeRate_df = pd.DataFrame(ustw_ExchangeRate)
    FundData_df = pd.merge(FundData_df, ustw_ExchangeRate_df[['InterbankRate', 'date']], on=['date'], how='left')
    FundData_df = FundData_df[['displayNameLocal', 'nav', 'tradeDate', 'date', 'InterbankRate']].copy()
    FundData_df['tw_nav'] = FundData_df['nav'] * FundData_df['InterbankRate']


    FundData['ustw_Rate'] = [ustw_ExchangeRate['InterbankRate'][ustw_ExchangeRate['date'].index(d)] if d in ustw_ExchangeRate['date'] else None for d in FundData['date']]

    tmp = pd.DataFrame(FundData)
    tmp = tmp[['displayNameLocal', 'nav', 'tradeDate', 'date', 'ustw_Rate']].copy()
    tmp['q'] = tmp['date'].map(lambda x: transform_StringDate2TimeStamp(x)*1000)
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