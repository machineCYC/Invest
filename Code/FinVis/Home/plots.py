import requests
import pandas as pd

from Home.plot.Index import *

def get_Api_Data(dataset, stock_id, date):
    url = 'http://finmindapi.servebeer.com/api/data'
    form_data = {'dataset':dataset,'stock_id':[stock_id],'date':date}
    res = requests.post(url,verify = True,data = form_data)
    temp = res.json()
    data = pd.DataFrame(temp['data'])
    return data