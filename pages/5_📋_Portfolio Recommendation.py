import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance
from PIL import Image
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Portfolio Recommendation System",page_icon="📋")
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
st.sidebar.header('Get Recommended Profile')
import numpy as np
import datetime
import time
import requests
from streamlit_lottie import st_lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
st.title('PORTFOLIO RECOMMENDATION SYSTEM :clipboard:')
lottie_tree = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_qxdztkhq.json")
st_lottie(lottie_tree, height=270, width=700)
st.sidebar.subheader('Choose Investor profile')
type_inv = st.sidebar.selectbox('Select Your Type',('Conservative', 'Mildly Conservative','Moderate','Mildly Aggressive','Aggressive'))
if type_inv=="Conservative":
    mul=0.05
    fi=0.85
    oth=0.1
elif type_inv=="Mildly Conservative":
    mul = 0.20
    fi = 0.75
    oth = 0.05
elif type_inv == "Moderate":
    mul = 0.35
    fi = 0.6
    oth = 0.05
elif type_inv == "Mildly Aggressive":
    mul = 0.90
    fi = 0.0
    oth = 0.1
else:
    mul= 0.95
    fi = 0.0
    oth = 0.05
amt=st.sidebar.number_input('Enter Total Amount You Want To Invest(Rs)')
st.sidebar.subheader('Equity Allocation')
tickers=(
'APOLLOHOSP.NS','AAPL','ADANIENT.NS','AMZN','BAJAJ-AUTO.NS','BHARTIARTL.NS','BRITANNIA.NS','CIPLA.NS',
'COALINDIA.NS','GOOG','HDFCLIFE.NS',  'ICICIBANK.NS','INDUSINDBK.NS',  'ITC.NS','MARUTI.NS','MSFT',
'NESTLEIND.NS','RELIANCE.NS','TATASTEEL.NS','TCS.NS','TITAN.NS','TSLA',
 'ULTRACEMCO.NS','WIPRO.NS')
dropdown = st.sidebar.multiselect('Select A Minimum Of Two Stocks',tickers )
# Row A
st.markdown('### Your Profile')
col1, col2 = st.columns(2)
col1.metric(label="Amount In Equity Assets",value= amt)
col2.metric(label="Number of Investments(Equity)",value= len(dropdown))
st.write('---')
with st.expander('Click to Learn more about different Investor Profiles'):
    st.markdown('### Investor Profiles For Reference ')
    #image = Image.open(r"C:\Users\aiman\Downloads\investor profile.png")
    #new_image = image.resize((900, 400))
    st.image("https://www.principal.com.my/sites/default/files/inline-images/risk%20profile.png", caption='Investor profiles For Reference.Source : Pricipal Malaysia')
    st.write("Conservative : I want to keep my capital.My main priority is to safeguard my investments capital. I feel safe to invest provided my capital invested is exposed to very little risk. I am willing to accept a minimal or very low potential returns; as long as my investment capital is retained.")
    st.write("Mildly Conservative : I want to earn small returns.My primary goal is to gain some returns from investments capital. I am willing to accept returns that are potentially higher than banks’ fixed deposit rate as long as my investments capital is expose to minimal level risk.")
    st.write("Moderate : I want to reap moderate returns.My focus is to obtain moderate returns by diversifying my investments capital. I am convinced that in order to achieve potentially moderate returns I have to be prepared to take a moderate level of risk. I am willing to keep my capital and returns invested in the short to medium term. I want to see my investments grow and increase over the long-term.")
    st.write("Mildly Aggressive : I want to secure high returns.My desire is to achieve high returns and understand the “high risk, high returns” trade off. I am confident that to purse potentially high returns over the long term, I must anticipate higher risk. I am willing to keep my capital and returns invested in the short to medium term. I want to see my investments grow and increase over the long-term. ")
    st.write("Aggressive : I want to achieve very high returns.My aim is to optimize the highest returns possible. I am bold to invest in high capital growth investments to yield potentially high returns over the long-term. I am prepared to be exposed to very high level of risk. I am willing to keep my capital and return invested in the medium to long-term as I want to see my investments grow and increase over the long-term.")
st.write('---')
start= datetime.datetime(2015,1,1)
end= datetime.datetime.today()
d={}
portf_vals=pd.DataFrame()
clicked2=st.sidebar.button('Recommend A Split')
if clicked2:
    if len(dropdown) > 1:
        for name in dropdown:
            d[name] = yfinance.download(name, start, end)
            df = yfinance.download(dropdown, start, end)['Adj Close']
            for stock_df in [d[name]]:
                stock_df['Normed Return'] = stock_df['Adj Close'] / stock_df.iloc[0]['Adj Close']
                stock_df['Allocation'] = stock_df['Normed Return']
                stock_df['Position Amount'] = stock_df['Allocation'] * 500000
    progress_bar = st.progress(0)
    if len(dropdown) > 1 and amt > 0:
        for perc_completed in range(100):
            time.sleep(0.05)
            progress_bar.progress(perc_completed + 1)

    if len(dropdown) > 1:
        for n in dropdown:
            total_pos_vals = [d[n]['Position Amount']]
            portf_vals = portf_vals.append(total_pos_vals)
            trans = portf_vals.T
            # portf_vals = pd.concat(total_pos_vals)
        trans['Total Pos'] = trans.sum(axis=1)
        trans1 = pd.DataFrame()
        trans1['Total Pos'] = trans['Total Pos']

        trans1['Daily Return'] = trans1['Total Pos'].pct_change(1)
        trans1.dropna(inplace=True)
        SR = trans1['Daily Return'].mean() / trans1['Daily Return'].std()
        print('Sharpe Ration = ', SR)
        # Annual Sharpe Ratio:
        ASR = (252 ** 0.5) * SR
        print('Annualized Sharpe Ratio = ', ASR)
        stocks = df
        stocks.pct_change(1).mean()
        log_returns = np.log(stocks / stocks.shift(1))
        num_ports = 5000
        all_weights = np.zeros((num_ports, len(stocks.columns)))
        ret_arr = np.zeros(num_ports)
        vol_arr = np.zeros(num_ports)
        sharpe_arr = np.zeros(num_ports)
        print(all_weights)
        for ind in range(num_ports):
            np.random.seed(0)
            weights = np.array(np.random.random(len(dropdown)))
            weights = weights / np.sum(weights)
            all_weights[ind, :] = weights
            ret_arr[ind] = np.sum((log_returns.mean() * weights) * 252)
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 252, weights)))
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]
        my_array = (all_weights[sharpe_arr.argmax(), :]*mul)
        fi1=1
        oth1=1
        my_array=np.append(my_array,fi)
        my_array = np.append(my_array, oth)
        rows = dropdown+['Fixed Income','Others']
        df = pd.DataFrame(my_array, index=rows)
        df = df.rename(columns={0: 'Percentage'})
        for ind in df.index:
            if ind=='Fixed Income':
                df['Amount To Invest(Rs.)'] = (df['Percentage']*amt)
                print(fi)
                print(oth)
            if ind=='Others':
                df['Amount To Invest(Rs.)'] = (df['Percentage']*amt)
                print(fi)
                print(oth)
            else:
                df['Amount To Invest(Rs.)'] = df['Percentage'] * amt
        df['Category Name'] = rows
        c1, c2 = st.columns((7, 3))
        with c1:
            fig = px.pie(df, names='Category Name', values='Percentage', hole=0.6, width=350, height=350,
                         title="Recommended Split Return vs Risk")
            st.plotly_chart(fig)
        with c2:
            st.write('')
            st.write(' Recommended Amount Return vs Risk')
            st.dataframe(data=df['Amount To Invest(Rs.)'])
        st.write(":information_source: Hover Over The Graph To See It's Interactive And Downloadable Features")
        st.write("---")
