import config
import datetime
import pandas as pd

from django.shortcuts import render
from Invest.Tool.load import receive_FinMindApi_JsonListData, receive_AnueApi_JsonListData
from Invest.Tool.common import transform_JsonList2ListJson, transform_Date2RecentWeekDays, transform_TimeStamp2StringDate, transform_StringDate2TimeStamp

def StockView(request):
    string_time = datetime.datetime.now().time().strftime("%H:%M")
    datetime_date = datetime.date.today() if string_time>='20:00' else datetime.date.today() - datetime.timedelta(days=1)
    string_date = transform_Date2RecentWeekDays(datetime_date)

    dataset = 'TaiwanStockPrice'

    context = []
    for stock_id in config.STOCK_ID_LIST:
        print(stock_id)
        signal_stock_data = receive_FinMindApi_JsonListData(dataset=dataset, stock_id=stock_id, date=string_date)
        context.extend(transform_JsonList2ListJson(signal_stock_data))
    return render(request, 'AssetStock.html', {'AssetStockList': context})

def FundView(request):
    string_date = transform_Date2RecentWeekDays(datetime.date.today())

    startAt = 1350230400
    # endAt = 1580140800
    endAt = transform_StringDate2TimeStamp(string_date)
    FundData = receive_AnueApi_JsonListData(startAt=startAt, endAt=endAt)
    FundData['date'] = list(map(lambda x: transform_TimeStamp2StringDate(x), FundData['tradeDate']))
    FundData['tradeDate'] = list(map(lambda x: ((x)*1000), FundData['tradeDate'])) # for Highcharts.stockChart timesteamp

    startDate = transform_TimeStamp2StringDate(startAt)
    ustw_ExchangeRate = receive_FinMindApi_JsonListData(dataset='ExchangeRate', data_id='Taiwan', date=startDate)

    FundData_df = pd.DataFrame(FundData)
    ustw_ExchangeRate_df = pd.DataFrame(ustw_ExchangeRate)

    data = pd.merge(FundData_df, ustw_ExchangeRate_df[['InterbankRate', 'date']], on=['date'], how='left')
    data['InterbankRate'] = data['InterbankRate'].interpolate()
    data['tw_nav'] = data['InterbankRate'] * data['nav']

    context = {}
    context['data'] = data[['tradeDate', 'nav']].values.tolist()
    context['pointInterval'] =  3600 * 1000 * 24
    context['pointStart'] =  min(FundData['tradeDate'])
    return render(request, 'AssetFund.html', context)

if __name__ == '__main__':
    import pandas as pd
    string_date = transform_Date2RecentWeekDays(datetime.date.today())
    startAt = 1350230400
    endAt = transform_StringDate2TimeStamp(string_date)
    FundData = receive_AnueApi_JsonListData(startAt=startAt, endAt=endAt)
    FundData_df = pd.DataFrame(FundData)

    startDate = transform_TimeStamp2StringDate(startAt)
    ustw_ExchangeRate = receive_FinMindApi_JsonListData(dataset='ExchangeRate', data_id='Taiwan', date=startDate)
    ustw_ExchangeRate_df = pd.DataFrame(ustw_ExchangeRate)

    data = pd.merge(FundData_df, ustw_ExchangeRate_df[['InterbankRate', 'date']], on=['date'], how='left')

    print('GG')