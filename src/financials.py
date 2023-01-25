from millify import millify
import streamlit as st
import pandas as pd
import requests
import os

env = os.environ

API_KEY = env['ALPHA_VANTAGE_KEY']
BASE_URL = 'https://www.alphavantage.co/query?function='

@st.cache
def company_overview(symbol):
    url = f'{BASE_URL}OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json(), response.status_code


def daily_adjusted(symbol, outputsize='compact'):
    url = f'{BASE_URL}TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={outputsize}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json(), response.status_code

@st.cache
def income_statement(symbol, quarterly=True):
    url = f'{BASE_URL}INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        segments = 'quarterlyReports' if quarterly else 'annualReports'
        df = pd.DataFrame(response.json()[segments])
        df = df.T.applymap(millify_convert)
        return df, response.status_code
    
    return response.json(), response.status_code

@st.cache
def balance_sheet(symbol, quarterly=True) -> pd.DataFrame:
    url = f'{BASE_URL}BALANCE_SHEET&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        segments = 'quarterlyReports' if quarterly else 'annualReports'
        df = pd.DataFrame(response.json()[segments])
        df = df.T.applymap(millify_convert)
        return df, response.status_code

    return response.json(), response.status_code



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
        The number of decimal places to round to.
    
    Returns
    -------
    str, int, float
    """
    try:
        return millify(value, precision=precision)
    except:
        return value