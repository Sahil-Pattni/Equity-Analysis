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
        "About": 'Equity Analysis Tool'
    }
)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

input_container = st.container()  # Input (ticker)
info_container = st.container()   # Company Overview, Metrics, Candlestick Chart


def load_data(ticker):
    """
    Load data from the API and display it on the page.

    Parameters
    ----------
    ticker : str
        The ticker of the company to load data for.
    
    Returns
    -------
    None
    """
    logging.info('Loading data...')
    # Company Name, Address, Description
    overview, response_code_overview = fin.company_overview(ticker)
    # Daily Adjusted Prices
    daily_adjusted, response_code_daily = fin.daily_adjusted(ticker)
    
    if response_code_overview == 200 and response_code_daily == 200:
        try:
            info_container.empty()
            logging.info('Data loaded successfully.')
            # Company Info
            info_container.header(f"{overview['Name']} ({overview['Symbol']})")
            info_container.caption(f"{overview['Address']}")
            info_container.caption(f"{overview['Description']}")

            # --- Metrics --- #
            col1, col2, col3, col4 = info_container.columns(4)
            col1.metric(label='Price', value=eg.get_latest_price(daily_adjusted))
            col2.metric(label='Market Cap', value=millify(overview['MarketCapitalization'], precision=3))
            col3.metric(label='P/E Ratio', value=overview['PERatio'])
            col4.metric(label='Dividend Yield', value=overview['DividendYield'])
            
            # CandleStick Chart
            info_container.plotly_chart(
                eg.candlestick(daily_adjusted),
                use_container_width=True
            )
            
            # --- Income Statement & Balance Sheet --- #
            col1, col2 = info_container.columns(2)
            # Income Statement
            income_statement, response_code = fin.income_statement(ticker)
            if response_code == 200:
                col1.subheader('Income Statement')
                col1.dataframe(income_statement)
            
            # Balance Sheet
            balance_sheet, response_code = fin.balance_sheet(ticker)
            if response_code == 200:
                col2.subheader('Balance Sheet')
                col2.dataframe(balance_sheet)

        except Exception as e:
            # Print error message and stack trace
            logging.error(e, exc_info=True)
            info_container.error('API limit reached. Please try again in 13 seconds.')
    else:
        # NOTE: When exceeding API limits, the repsonse code is still 200,
        # but the response body contains an error message. Therefore, we
        # catch the error here and display it to the user.
        logging.error('Ticker not found. Please try again.')
    



# Input Container
with input_container:
    st.text_input('Enter a ticker', value='AAPL', max_chars=5, key='ticker')
    st.button('Submit', key='submit_button')

# Load data when the submit button is clicked
if st.session_state.submit_button:
    load_data(st.session_state.ticker)