import plotly.graph_objs as go

from plotly.subplots import make_subplots
from plotly.offline import plot

CONFIG = {'displayModeBar': False}

def vis_test():
    import pandas as pd
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

    trace0 = go.Scatter(
        mode = 'lines',
        name = 'AAPL High',
        x = df['Date'],
        y = df['AAPL.High'],
        line = go.scatter.Line(
            color = '#17BECF'
        )
    )

    trace1 = go.Scatter(
        mode = 'lines',
        name = 'AAPL Low',
        x = df['Date'],
        y = df['AAPL.Low'],
        line = go.scatter.Line(
            color = '#7F7F7F'
        )
    )

    data = [trace0, trace1]

    layout = go.Layout(
        title = 'Time Series with Custom Date-Time Format',
        xaxis = go.layout.XAxis(
            tickformat = '%d %B (%a)<br>%Y'
        )
    )

    fig = go.Figure(
        data=data,
        layout=layout
    )

    # py.iplot(fig, filename='using-tickformat-attribute-date')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False, config=CONFIG)

    return plot_div

def vis_0056(df):
    if len(df) == 0:
        return '暫無資料'

    df['20MA'] = df['close'].rolling(window=20).mean()
    df['60MA'] = df['close'].rolling(window=60).mean()
    df['120MA'] = df['close'].rolling(window=120).mean()

    trace1 = {
        "x": df['date'],
        "close": df['close'],
        "decreasing": {"line": {"color": "green"}},
        "high": df['max'],
        "increasing": {"line": {"color": "red"}},
        "low": df['min'],
        "name": "GS",
        "open": df['open'],
        "type": "candlestick",
    }
    trace2 = {
        "x": df['date'],
        "y": df['20MA'],
        "line": {"width": 1},
        "marker": {"color": "#E377C2"},
        "mode": "lines",
        "name": "20MA",
    }
    trace3 = {
        "x": df['date'],
        "y": df['60MA'],
        "line": {"width": 1},
        "marker": {"color": "#77e38b"},
        "mode": "lines",
        "name": "60MA",
    }
    trace4 = {
        "x": df['date'],
        "y": df['120MA'],
        "line": {"width": 1},
        "marker": {"color": "#e3b677"},
        "mode": "lines",
        "name": "120MA",
    }
    trace5 = {
        'x': df['date'],
        'y': (df['Trading_Volume'] / 1000).astype(int),
        'marker': {'color': '#040273'},
        "type": "bar",
        "name": "vol",
        'yaxis': "y2",
    }
    data = [trace1, trace2, trace3, trace5]

    layout = {
        'title':'ETF(0056) 指數',
        'height': 800,
        'xaxis': {
            "rangeselector": {
                "x": 0,
                "y": 0.9,
                "bgcolor": "rgba(150, 200, 250, 0.4)",
                "buttons": [
                    {
                        "count": 1,
                        "label": "reset",
                        "step": "all"
                    },
                    {
                        "count": 1,
                        "label": "1M",
                        "step": "month",
                        "stepmode": "backward"
                    },
                    {
                        "count": 6,
                        "label": "6M",
                        "step": "month",
                        "stepmode": "backward"
                    },
                    {
                        "count": 1,
                        "label": "1Y",
                        "step": "year",
                        "stepmode": "backward"
                    },
                    {
                        "count": 3,
                        "label": "3Y",
                        "step": "year",
                        "stepmode": "backward"
                    },
                    {
                        "count": 5,
                        "label": "5Y",
                        "step": "year",
                        "stepmode": "backward"
                    },
                ],
                "font": {"size": 13}
            },
        },
        'yaxis':{
            'domain': [0.3, 1]
        },
        'yaxis2':{
            'domain': [0, 0.2]
        },
    }

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False, config=CONFIG)

    return plot_div

