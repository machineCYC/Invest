import config
import datetime

from django.shortcuts import render
from Invest.Tool.load import receive_FinMindApi_JsonListData, receive_AnueApi_JsonListData
from Invest.Tool.common import transform_JsonList2ListJson, transform_Data2RecentWeekDays

def StockView(request):
    date = transform_Data2RecentWeekDays(datetime.date.today())
    datadet = 'TaiwanStockPrice'

    context = []
    for stock_id in config.STOCK_ID_LIST:
        signal_stock_data = receive_FinMindApi_JsonListData(datadet=datadet, stock_id=stock_id, date=date)
        context.extend(transform_JsonList2ListJson(signal_stock_data))

    return render(request, 'AssetStock.html', {'AssetStockList': context})

def FundView(request):
    date = transform_Data2RecentWeekDays(datetime.date.today())

    startAt = 1350230400
    endAt = 1580140800
    data = receive_AnueApi_JsonListData(startAt=startAt, endAt=endAt)
    print(data)
    return render(request, 'AssetFund.html', {'AssetFundList': data})