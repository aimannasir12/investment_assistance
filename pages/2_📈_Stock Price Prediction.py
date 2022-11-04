import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import yfinance as yf
from datetime import date
import requests
import pandas as pd
from streamlit_lottie import st_lottie
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# to configure streamlit webapp aesthetics
st.set_page_config(page_title="Welcome to our Small Investor Assistant",page_icon="📈",layout='centered')
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
st.markdown("<h1 style='text-align: center; color: black;'>STOCK PRICE PREDICTION</h1>", unsafe_allow_html=True)
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
lottie_stocks = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_wh4gk3bb.json")
st_lottie(lottie_stocks, height=270, width=700)
st.write("Visualise The Predicted Price Of A Stock Based On Factors Such As The Company's Financial Performance Over A Period Of Your Choice.! We Have Provided Information For Popular Indian And U.S. Stocks")
st.write("Select A Stock From The Menu And Move The Slider Around To Select The Number Of Years You Want The Prediction For.The Plots Generated Are Interactive And Downloadable, So Feel Free To Play Around.:wink:")
stocks = (
'APOLLOHOSP.NS','AAPL','ADANIENT.NS','AMZN','BAJAJ-AUTO.NS','BHARTIARTL.NS','BRITANNIA.NS','CIPLA.NS',
'COALINDIA.NS','GOOG','HDFCLIFE.NS',  'ICICIBANK.NS','INDUSINDBK.NS',  'ITC.NS','MARUTI.NS','MSFT',
'NESTLEIND.NS','RELIANCE.NS','TATASTEEL.NS','TCS.NS','TITAN.NS','TSLA',
 'ULTRACEMCO.NS','WIPRO.NS')
selected_stock = st.selectbox('What stock are you looking for?', stocks)
n_years = st.slider('Years of prediction:', 1, 5)
clicked=st.button('Predict')
if clicked:
    period = n_years * 365


    # to load the yfinance data to the webapp
    @st.cache(allow_output_mutation=True)
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    # When the user selects a specific stock its data is loaded
    data = load_data(selected_stock)
    data['Date'] = data['Date'].dt.tz_localize(None)
    last_column = data['Close']
    todays = last_column[len(data) - 1]
    yesterdays = last_column[len(data) - 2]
    changed = ((todays - yesterdays) / yesterdays) * 100
    changed1='{0:.2f}'.format(changed)
    if (todays - yesterdays) > 0:
        st.success(f'This stock showed a rise in price today by {changed1}% !! 	:chart_with_upwards_trend:')
    else:
        st.error(f'This stock showed a drop in price today by {changed1}% !! 	:chart_with_downwards_trend:')
    st.write("---")
    st.header(f'Forecast plot for {n_years} years')
    data_load_state = st.text('Forecasting data...')
    # A dataframe is created for fbprofhet that makes fute predictions based on the user input
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    model = Prophet()
    model.fit(df_train)
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)
    fig1 = model.plot(forecast)
    plot_plotly(model, forecast)
    data_load_state.text('')
    # The forecasts are plotted on the website
    fig1 = plot_plotly(model, forecast)
    st.plotly_chart(fig1)
    st.write(":information_source: Hover Over The Graph To See It's Interactive And Downloadable Features")
    st.write("---")
    st.header("Financial Indicators And Recommended Actions")
    symbol = yf.Ticker(selected_stock).info
    import plotly.graph_objects as go
    if 'currentPrice' in symbol.keys():
        i0 = symbol['currentPrice']
        st.write(f"Current Stock Price : {i0}")
    if 'financialCurrency' in symbol.keys():
        i1 = symbol['financialCurrency']
        st.write(f"Currency : {i1}")
    if 'industry' in symbol.keys():
        i2 = symbol['industry']
        st.write(f"Industry : {i2}")
    if 'dividendYield' in symbol.keys():
        i5 = symbol['dividendYield']
        st.write(f"Dividend : {i5}")
    if 'morningStarOverallRating' in symbol.keys():
        i6 = symbol['morningStarOverallRating']
        st.write(f"Stock Rating : {i6}")
    if 'fiftyDayAverage' in symbol.keys():
        i6 = symbol['fiftyDayAverage']
        st.write(f"50 Day Average : {i6}")
    if 'recommendationKey' in symbol.keys():
        i7 = symbol['recommendationKey']
        st.write(f"Recommendation : {i7}")
    indicators_load_state = st.text('Calculating Indicators...')
    c1, c2 = st.columns((7, 3))
    import numpy as np
    plot_bgcolor = "#FFFFFF"
    quadrant_colors = [plot_bgcolor, "#f25829", "#f2a529", "#eff229", "#85e043", "#2bad4e"]
    quadrant_text = ["", "<b>Strong Sell</b>", "<b>Sell</b>", "<b>Neutral</b>", "<b>Buy</b>", "<b>Strong Buy</b>"]
    n_quadrants = len(quadrant_colors) - 1
    if 'trailingPE' in symbol.keys():
        pe = symbol["trailingPE"]
        if isinstance(pe, float):
            current_value1 = pe
            min_value = 0
            max_value = 50
            hand_length = np.sqrt(2) / 4
            hand_angle1 = np.pi * (1 - (max(min_value, min(max_value, current_value1)) - min_value) / (max_value - min_value))
            fig3 = go.Figure(
                   data=[
                       go.Pie(
                           values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                           rotation=90,
                           hole=0.5,
                           marker_colors=quadrant_colors,
                           text=quadrant_text,
                           textinfo="text",
                           hoverinfo="skip",
                       ),
                   ],
                   layout=go.Layout(
                       showlegend=False,
                       margin=dict(b=0, t=10, l=10, r=10),
                       width=450,
                       height=450,
                       paper_bgcolor=plot_bgcolor,
                       annotations=[
                           go.layout.Annotation(
                               text=f"<b>P/E Ratio:</b><br>{current_value1} units",
                               x=0.5, xanchor="center", xref="paper",
                               y=0.25, yanchor="bottom", yref="paper",
                               showarrow=False,
                           )
                       ],
                       shapes=[
                           go.layout.Shape(
                               type="circle",
                               x0=0.48, x1=0.52,
                               y0=0.48, y1=0.52,
                               fillcolor="#333",
                               line_color="#333",
                           ),
                           go.layout.Shape(
                               type="line",
                               x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle1),
                               y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle1),
                               line=dict(color="#333", width=4)
                           )
                       ]
                   )
               )
            fig3.update_layout(
               autosize=False,
               width=300,
               height=300)
            with c1:
                st.plotly_chart(fig3)
    indicators_load_state.text('')
    if 'debtToEquity' in symbol.keys():
        de = symbol["debtToEquity"]*0.01
        if isinstance(de, float):
           current_value2 = de
           min_value = 0
           max_value = 3
           hand_length = np.sqrt(2) / 4
           hand_angle2 = np.pi * (1 - (max(min_value, min(max_value, current_value2)) - min_value) / (max_value - min_value))
           fig2 = go.Figure(data=[go.Pie(
                            values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                            rotation=90,
                            hole=0.5,
                            marker_colors=quadrant_colors,
                            text=quadrant_text,
                            textinfo="text",
                            hoverinfo="skip",),],
                    layout=go.Layout(
                        showlegend=False,
                        margin=dict(b=0, t=10, l=10, r=10),
                        width=450,
                        height=450,
                        paper_bgcolor=plot_bgcolor,
                        annotations=[
                            go.layout.Annotation(
                                text=f"<b>Debt To Equity Ratio:</b><br>{current_value2} units",
                                x=0.5, xanchor="center", xref="paper",
                                y=0.25, yanchor="bottom", yref="paper",
                                showarrow=False,
                            )
                        ],
                        shapes=[
                            go.layout.Shape(
                                type="circle",
                                x0=0.48, x1=0.52,
                                y0=0.48, y1=0.52,
                                fillcolor="#333",
                                line_color="#333",
                            ),
                            go.layout.Shape(
                                type="line",
                                x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle2),
                                y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle2),
                                line=dict(color="#333", width=4)
                            )
                        ]
                    )
                )
           fig2.update_layout(
                autosize=False,
                width=300,
                height=300)
           with c2:
            st.plotly_chart(fig2)
    if 'currentPrice' in symbol.keys():
        if 'fiftyDayAverage' in symbol.keys():
            cp = symbol['currentPrice']
            fda = symbol['fiftyDayAverage']
            changed1 = (cp - fda) / cp * 100
            changed2 = '{0:.2f}'.format(changed1)
    if changed1>0:
        st.error(f"The Stock Price Is Up By {changed2} % Compared To It's Average Trading Price For The Past 50 Days In Case You Are Looking To Buy A Stock Now's Probably Not A Great Time")
    else:
        st.success(f"The Stock Price Is Down By {changed2} % Compared To It's Average Trading Price For The Past 50 Days In Case You Are Looking To Buy A Stock Now's Probably A Great Time")
    with st.expander('Click to Learn More About What Different Ratios Mean'):
        st.markdown('### Ratios And Their Meanings: ')
        st.write("---")
        st.write("Dividend : The dividend yield is a financial ratio that tells you the percentage of a company's share price that it pays out in dividends each year.")
        st.write("Stock Rating : a measure of the performance of a stock in a given specific time period.This is given by Morning Star ")
        st.write("P/E Ratio : the ratio of share price of a stock to its earnings per share (EPS). PE ratio is one of the most popular valuation metric of stocks. It provides indication whether a stock at its current market price is expensive or cheap. Buying a stock at a low P/E ratio means great growth potential")
        st.write("Debt To Equity Ratio : ratio that compares a company's debt obligations (both short-term debt and long-term debt) to the company's total assets. Indicates the solvency risk associates with the stock. For big companies a higher ratio is also acceptable")