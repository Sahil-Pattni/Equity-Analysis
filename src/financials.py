import streamlit as st
import requests
import os

env = os.environ

API_KEY = env['ALPHA_VANTAGE_KEY']
BASE_URL = 'https://www.alphavantage.co/query?function='

def company_overview(symbol):
    url = f'{BASE_URL}OVERVIEW&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json(), response.status_code


def daily_adjusted(symbol, outputsize='compact'):
    url = f'{BASE_URL}TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={outputsize}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json(), response.status_code