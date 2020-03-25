import config
import datetime
import pandas as pd

from django.shortcuts import render
from django.views.generic import TemplateView
from Invest.Tool.load import receive_FinMindApi_JsonListData, receive_AnueApi_JsonListData
from Invest.Tool.common import transform_JsonList2ListJson, transform_Date2RecentWeekDays, transform_TimeStamp2StringDate, transform_StringDate2TimeStamp

class Fund(TemplateView):
    def __init__(self):
        self.template_name = r'/mnt/d/personal_workspace/Invest/Invest/Home/templates/AssetFund.html'
        self.fundID = 'B20%2C073'
        self.startAt = 1350230400
        self.response_context = {}
        print('init:{}'.format(self.fundID))
    
    def post(self, request, *args, **kwargs):
        self.fundID = request.POST.get('fundname', '')
        print(self.fundID)
        if self.fundID == '':
            # return error page
            pass
        else:
            string_date = transform_Date2RecentWeekDays(datetime.date.today())
            endAt = transform_StringDate2TimeStamp(string_date)

            FundData = receive_AnueApi_JsonListData(startAt=self.startAt, fundName=self.fundID)
            utc_delta = 60 * 60 * 8
            FundData['date'] = list(map(lambda x: transform_TimeStamp2StringDate(x+utc_delta), FundData['tradeDate']))
            FundData['tradeDate'] = list(map(lambda x: ((x+utc_delta)*1000), FundData['tradeDate'])) # for Highcharts.stockChart timesteamp

            startDate = transform_TimeStamp2StringDate(self.startAt)
            ustw_ExchangeRate = receive_FinMindApi_JsonListData(dataset='TaiwanExchangeRate', data_id='USD', date=startDate)

            FundData_df = pd.DataFrame(FundData)
            ustw_ExchangeRate_df = pd.DataFrame(ustw_ExchangeRate)

            data = pd.merge(FundData_df, ustw_ExchangeRate_df[['spot_sell', 'date']], on=['date'], how='left')
            data['spot_sell'] = data['spot_sell'].interpolate()
            data['tw_nav'] = data['spot_sell'] * data['nav']
            print(data[['date', 'tw_nav', 'nav', 'spot_sell', 'tradeDate']])
            
            response_context = {}
            response_context['displayNameLocal'] = FundData['displayNameLocal']
            response_context['data'] = data[['tradeDate', 'tw_nav']].values.tolist()
            response_context['pointInterval'] =  3600 * 1000 * 24
            response_context['pointStart'] =  min(FundData['tradeDate'])
        return render(request, 'AssetFund.html', response_context)

def IndexView(request):
    print('This is index')
    FundReports = r'/mnt/d/personal_workspace/Invest/Data/Report/AnueFundReport_2020-03-14.csv'
    context = {}
    context['data'] = FundReports
    print(context)
    return render(request, 'index.html', {'table': context})

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

if __name__ == '__main__':
    string_date = transform_Date2RecentWeekDays(datetime.date.today())
    startAt = 1350230400
    endAt = transform_StringDate2TimeStamp(string_date)
    fund_name = 'B33%2C120'
    FundData = receive_AnueApi_JsonListData(startAt=startAt, fundName=fund_name)
    FundData['date'] = list(map(lambda x: transform_TimeStamp2StringDate(x), FundData['tradeDate']))
    FundData_df = pd.DataFrame(FundData)

    startDate = transform_TimeStamp2StringDate(startAt)
    ustw_ExchangeRate = receive_FinMindApi_JsonListData(dataset='TaiwanExchangeRate', data_id='USD', date=startDate)
    ustw_ExchangeRate_df = pd.DataFrame(ustw_ExchangeRate)
    data = pd.merge(FundData_df, ustw_ExchangeRate_df[['spot_sell', 'date']], on=['date'], how='left')

    print('GG')