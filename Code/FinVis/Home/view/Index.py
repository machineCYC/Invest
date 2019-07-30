import numpy as np
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse
from Home import plots
from django.views.generic import TemplateView

def cal_RSV_Value(stock_price, days=9):
    sp = stock_price

    data = pd.DataFrame()
    data['rolling_min'] = sp['min'].rolling(window = days).min()
    data['rolling_max'] = sp['max'].rolling(window = days).max()
    data['close'] = sp['close']
    data['date'] = sp['date']
    rsv = (data['close'] - data['rolling_min'])/(data['rolling_max']-data['rolling_min'])
    rsv = round(rsv, 2)*100

    return rsv

def cal_KD_Value(df):
    df['rsv'] = cal_RSV_Value(stock_price=df, days=9)
    rsv = df['rsv'].values
    rsv_na = rsv[np.isnan(rsv)]
    rsv = rsv[~np.isnan(rsv)]

    result = {'K_val':[50], 'D_val':[50]}
    K_val_list = [50]
    D_val_list = [50]
    for i in range(1, len(rsv)):
        K_value = (1/3) * rsv[i] + (2/3) * K_val_list[i-1]
        K_val_list.append(K_value)
        D_value = (2/3) * D_val_list[i-1] + (1/3) * K_val_list[i]
        D_val_list.append(D_value)
    return np.append(rsv_na, np.array(K_val_list)), np.append(rsv_na, np.array(D_val_list))

def Index(request):
    date = '2018-01-01'
    sto_pri_0056_df = plots.get_Api_Data(dataset='TaiwanStockPrice', stock_id='0056', date=date)
    sto_pri_twii_df = plots.get_Api_Data(dataset='TaiwanStockPrice', stock_id='^TWII', date=date)
    sto_pri_twii_df['K9'],  sto_pri_twii_df['D9'] = cal_KD_Value(sto_pri_twii_df)

    context = {}
    context['plot_0056'] = plots.vis_0056(sto_pri_0056_df, sto_pri_twii_df)
    context['plot_TWII'] = plots.vis_Twii(sto_pri_twii_df)
    # context['plot'] = plots.vis_test()
    return render(request, 'Index.html', context)

def Test(request):
    return HttpResponse(u"歡迎光臨!")