# %%
import plotly.graph_objects as go
import financials as fin
import plotly.express as px
import pandas as pd
import numpy as np
import json


# --- HELPER METHODS --- #
def __extract_daily_price(data: dict) -> pd.DataFrame:
    """
    Gets the second key in the dict, which is the daily price data.

    Parameters
    ----------
    data : dict
        The data to extract the daily price data from.

    Returns
    -------
    pd.DataFrame
    """
    return pd.DataFrame(data[list(data.keys())[1]])


def get_latest_price(data: dict) -> float:
    """
    Gets the latest price from the daily price data.

    Parameters
    ----------
    data : dict
        The data to extract the latest price from.

    Returns
    -------
    float
    """
    return float(__extract_daily_price(data).T['4. close'].iloc[0])


def get_date_only(date: pd.Timestamp):
    """
    Gets the date only from a pd.Timestamp.

    Parameters
    ----------
    date : pd.Timestamp
        The date to get the date only from.

    Returns
    -------
    str
    """
    return date.strftime('%b %d, %Y')


def line_chart(data: dict) -> px.line:
    """
    Generates a line chart from the daily price data.

    Parameters
    ----------
    data : dict
        The daily price data to generate the line chart from.

    Returns
    -------
    px.line
    """
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


def candlestick(data: dict) -> go.Figure:
    """
    Generates a candlestick chart from the daily price data.

    Parameters
    ----------
    data : dict
        The daily price data to generate the candlestick chart from.

    Returns
    -------
    go.Figure
    """
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
