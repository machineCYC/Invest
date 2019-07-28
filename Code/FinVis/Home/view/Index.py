from django.shortcuts import render
from django.http import HttpResponse
from Home import plots

def Index(request):
    sto_pri_df = plots.get_Api_Data(dataset='TaiwanStockPrice', stock_id='0056', date='2015-01-01')
    # sto_pri_df = plots.get_Api_Data(dataset='TaiwanStockPrice', stock_id='0056', date='2015-01-01')

    context = {}
    context['plot'] = plots.vis_0056(sto_pri_df)
    # context['plot'] = plots.vis_test()
    return render(request, 'Index.html', context)

def Test(request):
    return HttpResponse(u"歡迎光臨!")