import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import element_generator as eg
import financials as fin
import time
import logging
from millify import millify


# Page Config
st.set_page_config(
    page_title="Equity Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": 'COOLK'
    }
)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

# --- GLOBALS --- #
# Containers

container_one = st.container()
container_two = st.container()



def load_data(ticker):
    logging.info('Loading data...')
    overview, response_code = fin.company_overview(ticker)
    daily_adjusted, _ = fin.daily_adjusted(ticker)
    if response_code == 200:
        container_two.empty()
        logging.info('Data loaded successfully.')
        container_two.header(f"{overview['Name']} ({overview['Symbol']})")
        container_two.caption(f"{overview['Address']}")
        container_two.caption(f"{overview['Description']}")

        # --- Metrics --- #
        col1, col2, col3 = container_two.columns(3)
        col1.metric(label='Market Cap', value=millify(overview['MarketCapitalization'], precision=3))
        col2.metric(label='P/E Ratio', value=overview['PERatio'])
        col3.metric(label='Dividend Yield', value=overview['DividendYield'])

        
    else:
        logging.error('Ticker not found. Please try again.')
    



with container_one:
    st.text_input('Enter a ticker', value='AAPL', max_chars=5, key='ticker')
    st.button('Submit', key='submit_button')

if st.session_state.submit_button:
    load_data(st.session_state.ticker)