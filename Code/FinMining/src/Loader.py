import requests
import pandas as pd


def get_data(dataset_name, stock_id='', start_date='', end_date=''):
    '''
    Args:
        dataset_name: (str)
        stock_id: (list)
        start_date: (str)
        end_date: (str)

    Returns:
        api_data: (dict)
    '''
    url = 'http://finmindapi.servebeer.com/api/data'

    form_data = {
        'dataset': dataset_name,
        'stock_id': stock_id,
        'date': start_date
    }
    res = requests.post(url, verify=True, headers={}, data=form_data)

    api_data = res.json()

    if api_data['status_msg'] == 'ok':
        data = pd.DataFrame(api_data['data'])

    if end_date:
        data = data[data['date'] < end_date].reset_index(drop=True)

    return data