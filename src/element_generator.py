# %%
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import financials as fin
import json


# --- HELPER METHODS --- #
def __extract_daily_price(data: dict) -> pd.DataFrame:
    # Get the second key in the dict, which is the daily price data
    return pd.DataFrame(data[list(data.keys())[1]])


def get_latest_price(data: dict) -> float:
    return float(__extract_daily_price(data).T['4. close'].iloc[0])

def get_date_only(date: pd.Timestamp):
    return date.strftime('%b %d, %Y')

def line_chart(data: dict):
    df = __extract_daily_price(data).T
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    
    return px.line(
        df, 
        x=df.index, 
        y='4. close', title=f'{get_date_only(df.index[-1])} to {get_date_only(df.index[0])}',
        labels={
            '4. close': 'Price (USD)',
            'variable': 'Metric',
            'index': 'Date',
        },
    )

def candlestick(data: dict):
    df = __extract_daily_price(data).T
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    
    return go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df['1. open'],
                high=df['2. high'],
                low=df['3. low'],
                close=df['4. close'],
            )
        ],
        layout=go.Layout(
            title=f'Daily prices from {get_date_only(df.index[-1])} to {get_date_only(df.index[0])}',
            yaxis_title='Price (USD)',
        )
    )

