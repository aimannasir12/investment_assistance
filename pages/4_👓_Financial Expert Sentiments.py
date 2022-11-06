import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
st.set_page_config(page_title="Welcome To Our Small Investor Advisor",page_icon="👓")
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
st.title('FINANCIAL NEWS SENTIMENT ANALYSIS:newspaper:')
lottie_stocks = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_q7ia4fyk.json")
st_lottie(lottie_stocks, height=270, width=700)
st.write('Hear both good and bad about the market and want to get a total estimate on the good and the bad?')
st.write('Do not worry..we will scrape the web for financial news and analyzed the positive and negatives that are being said about your favourite futures.')
finviz_url = 'https://finviz.com/quote.ashx?t='
tickers=['OIL','GOLD','DOW','ES','HDB','IBN','INFY','TTM','WIT','AAPL','AMZN','GOOG','MSFT','TSLA']
dropdown = st.multiselect('Select One Or More Stocks/Futures/Forex You Want Financial News Sentiment Analysis For :-',tickers )
clicked1=st.button('Predict')
with st.expander('Click If You Are Unfamiliar With Any Of The Above Symbols'):
    st.write("DOW:Dow Jones Industry Average")
    st.write("ES:S&P 500")
    st.write("HDB:HDFC Bank Limited")
    st.write("IBN:ICICI Bank Limited")
    st.write("INFY:Infosys Limited")
    st.write("INFY:Tata Motors Limited")
    st.write("WIT:Wipro Limited")
if clicked1:
    with st.spinner('This may take a little while...'):
        time.sleep(5)
    st.success('Done scraping!')
    st.info(':information_source: Scroll down to obtain the data..:clock4:')
    if len(dropdown) > 0:
        news_tables = {}
        df = pd.read_csv(r"C:\Users\aiman\PycharmProjects\investment_assistance\df.csv")
        df1 = pd.DataFrame()
        want = dropdown
        for wants in want:
            for index, row in df.iterrows():
                if wants == row["ticker"]:
                    df1 = df1.append(row, ignore_index=True)
        nltk.download('vader_lexicon')
        vader = SentimentIntensityAnalyzer()
        f = lambda title: vader.polarity_scores(title)['compound']
        df1['compound'] = df1['title'].apply(f)
        df1['date'] = pd.to_datetime(df1.date).dt.date
        fig = plt.figure(figsize=(10, 20))
        mean_df = df1.groupby(['ticker', 'date']).mean().unstack()
        mean_df = mean_df.xs('compound', axis="columns")
        mean_df.plot(kind='bar')
        # plt.legend().set_visible(False)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 3})
        plt.show()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.write('---')
        st.subheader('In the news:-')
        st.pyplot()
        st.write(
            ':information_source: We have visualized the positive and negative sentiment being expressed by the news datewise for the past 6 months.')
        st.write("---")



