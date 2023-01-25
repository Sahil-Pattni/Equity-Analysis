from millify import millify
from typing import Tuple
import streamlit as st
import pandas as pd
import requests
import os

env = os.environ

API_KEY = env['ALPHA_VANTAGE_KEY']
BASE_URL = 'https://www.alphavantage.co/query?function='


@st.cache
def company_overview(symbol) -> Tuple(dict, int):
    """
    Gets the company overview data from the API.

    Parameters
    ----------
    symbol : str
        The ticker of the company to get the overview for.

    Returns
    -------
    dict, int
    """
    url = f'{BASE_URL}OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json(), response.status_code


def daily_adjusted(symbol, outputsize='compact') -> Tuple(dict, int):
    """
    Gets the daily adjusted prices from the API.

    Parameters
    ----------
    symbol : str
        The ticker of the company to get the prices for.
    outputsize : str
        The size of the output. Can be 'compact' or 'full'.

    Returns
    -------
    dict, int
    """
    url = f'{BASE_URL}TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={outputsize}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json(), response.status_code


@st.cache
def income_statement(symbol, quarterly=True) -> Tuple(pd.DataFrame, int):
    """
    Gets the income statement from the API.

    Parameters
    ----------
    symbol : str
        The ticker of the company to get the income statement for.
    quarterly : bool
        Whether to get the quarterly or annual income statements.

    Returns
    -------
    pd.DataFrame, int
    """
    url = f'{BASE_URL}INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        segments = 'quarterlyReports' if quarterly else 'annualReports'
        df = pd.DataFrame(response.json()[segments])
        df = df.T.applymap(millify_convert)
        return df, response.status_code

    return None, response.status_code


@st.cache
def balance_sheet(symbol, quarterly=True) -> Tuple(pd.DataFrame, int):
    """
    Gets the balance sheet from the API.

    Parameters
    ----------
    symbol : str
        The ticker of the company to get the balance sheet for.
    quarterly : bool
        Whether to get the quarterly or annual balance sheets.

    Returns
    -------
    pd.DataFrame, int
    """
    url = f'{BASE_URL}BALANCE_SHEET&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        segments = 'quarterlyReports' if quarterly else 'annualReports'
        df = pd.DataFrame(response.json()[segments])
        df = df.T.applymap(millify_convert)
        return df, response.status_code

    return None, response.status_code


# --- HELPER FUNCTIONS --- #
def millify_convert(value, precision=2):
    """
    Attempts to convert a value to a millified value.
    If it fails, it returns the original value.

    Parameters
    ----------
    value : str, int, float
        The value to convert.
    precision : int
        The number of decimal places to round to (Default: 2).

    Returns
    -------
    str, int, float
    """
    try:
        return millify(value, precision=precision)
    except:
        return value
