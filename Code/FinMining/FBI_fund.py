import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.Loader import get_data
from src.analysis import Smoothing

from FinMind.Data import Load
ExchangeRate_list = Load.FinDataList(dataset = 'ExchangeRate')
data = Load.FinData(dataset = 'ExchangeRate', select = 'Taiwan',date = '2018-10-10')

ExchangeRate = get_data(dataset_name='ExchangeRate', stock_id='Taiwan')


us_sp500_df = get_data(dataset_name='USStockPrice', stock_id='^GSPC', start_date='2018-01-01')
us_sp500_df = us_sp500_df[['date', 'stock_id', 'Adj_Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
us_sp500_df.columns = [str(col).lower() for col in us_sp500_df.columns]
us_sp500_df['ma20'] = Smoothing().moving_means(us_sp500_df['close'].values, 20)
us_sp500_df['bias20'] = (us_sp500_df['close'].values - us_sp500_df['ma20'].values) / us_sp500_df['ma20'].values
us_sp500_df = us_sp500_df[~us_sp500_df['ma20'].isna()]
us_sp500_df['bias20'] = (us_sp500_df['bias20'] * 100).astype(int)
us_sp500_df = us_sp500_df.reset_index(drop=True)
us_sp500_df['x_pos'] = us_sp500_df.index


### visulization
fig = plt.figure(figsize=(18, 9), facecolor='.6')
axes = fig.add_subplot(111)
axes.plot(us_sp500_df['x_pos'].values, us_sp500_df['close'].values,
            lw=2, c="b", label='TWII', marker="o", alpha=0.5)
axes.plot(us_sp500_df['x_pos'].values, us_sp500_df['ma20'].values,
            lw=2, c="r", label='ma20', alpha=0.5)

for label in axes.xaxis.get_ticklabels():
    label.set_rotation(90)
axes.set_xticks(us_sp500_df['x_pos'].values+0.1)
axes.set_xticklabels(us_sp500_df['date'].values, rotation=90)
axes.legend()

# axes2 = fig.add_subplot(212)
axes2 = axes.twinx()
axes2.plot(us_sp500_df['x_pos'].values, us_sp500_df['bias20'].values,
            lw=2, c="g", label='bias20', marker="_", alpha=0.5)

axes2.axhline(y=0, c='m', ls='--', alpha=0.4)
axes2.axhline(y=-5, c='m', ls='--', alpha=0.6)
axes2.axhline(y=-10, c='m', ls='--', alpha=0.8)
axes2.axhline(y=-15, c='m', ls='--', alpha=1.0)
axes2.set_yticks(np.arange(-15,40,5))
axes2.set_yticklabels(np.arange(-15,40,5))
axes2.grid(False)
plt.tight_layout()

file_name = 'GSPC_20180501_index.png'
# save_path = os.path.join(config['DirPath']['DrawPlot'], file_name)

# fig.savefig(save_path)
plt.show()
