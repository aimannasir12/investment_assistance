import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
st.set_page_config(layout='wide', initial_sidebar_state='expanded',page_title="Market Crash Prediction",page_icon="🔻")
st.markdown("<h1 style='text-align: center; color: black;'>MARKET CRASH PREDICTION DASHBOARD</h1>", unsafe_allow_html=True)
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
import requests
from streamlit_lottie import st_lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_tree = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qZHZpyb0Pd.json")
st_lottie(lottie_tree, height=350, width=900)
st.sidebar.subheader('Choose Parameters')
type_market = st.sidebar.selectbox('Select Market',('S&P500', 'BSE'))
months = st.sidebar.selectbox('Select Months For Prediction',('1', '3','6'))
previous = st.sidebar.checkbox('Show Performance On Previous Crashes')
details = st.sidebar.checkbox('Show Model Performance Details')
if type_market=="S&P500":
    if months=="1":
       image1 = Image.open(r"17-22(1).png")
       st.image(image1, caption="S&P500 Crash predictor for 1 month", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    if months=="3":
       image2 = Image.open(r"17-22(3).png")
       st.image(image2, caption="S&P500 Crash predictor for 3 months", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    if months=="6":
       image3 = Image.open(r"17-22(6).png")
       st.image(image3, caption="S&P500 Crash predictor for 6 months", width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    st.write("---")
    df = pd.DataFrame({"col_1": ['Confidence Score Of Crash Happening In 1 Month',
                                 'Confidence Score Of Crash Happening In 3 Months',
                                 'Confidence Score Of Crash Happening In 6 Months'], "col_2": [0.0, 1, 0.93]},
                      index=['Confidence Score Of Crash Happening In 1 Month',
                             'Confidence Score Of Crash Happening In 3 Months',
                             'Confidence Score Of Crash Happening In 6 Months'])
    fig = px.bar(df["col_1"], y=df["col_2"], )
    st.plotly_chart(fig)
    st.write("Confidence score of prediction of a crash within the next month 1 interval: 0.0")
    st.write("Confidence score of prediction of a crash within the next month 3 interval: 1.0")
    st.write("Confidence score of prediction of a crash within the next month 6 interval: 0.93")
    st.write("---")
    if previous:
       image4 = Image.open(r"04-10(6).png")
       st.image(image4, caption="Crash predictor Performance for 2004-2010", width=None, use_column_width=None, clamp=False,
                     channels="RGB", output_format="auto")
       image5 = Image.open(r"95-03(6).png")
       st.image(image5, caption="Crash predictor Performance for 1995-2003", width=None, use_column_width=None, clamp=False,
                channels="RGB", output_format="auto")
       image6 = Image.open(r"83-88(6).png")
       st.image(image6, caption="Crash predictor Performance for 1983-1988", width=None, use_column_width=None, clamp=False,
                channels="RGB", output_format="auto")
       image7 = Image.open(r"76-83(6).png")
       st.image(image7, caption="Crash predictor Performance for 1976-1983", width=None, use_column_width=None, clamp=False,
                channels="RGB", output_format="auto")
       image8 = Image.open(r"71-81(6).png")
       st.image(image8, caption="Crash predictor Performance 1971-1981", width=None, use_column_width=None, clamp=False,
                channels="RGB", output_format="auto")
       if details:
           st.header("Test Set Results:")
           st.write("Precision test (model/random):      0.26 / 0.15")
           st.write("Recall test (model/random):         0.74 / 0.44")
           st.write("Accuracy test (model/random):       0.64 / 0.54")
           st.write("Score test fbeta:                   0.54 / 0.32")
if type_market == "BSE":
        if months == "1":
            image1 = Image.open(r"17-22(1) b.png")
            st.image(image1, caption="S&P500 Crash predictor for 1 month", width=None, use_column_width=None,
                     clamp=False, channels="RGB", output_format="auto")
        if months == "3":
            image2 = Image.open(r"17-22(3) b.png")
            st.image(image2, caption="S&P500 Crash predictor for 3 months", width=None, use_column_width=None,
                     clamp=False, channels="RGB", output_format="auto")
        if months == "6":
            image3 = Image.open(r"19-22(6) b.png")
            #image3=image3a.rotate(90)
            st.image(image3, caption="S&P500 Crash predictor for 6 months", width=None, use_column_width=None,
                     clamp=False, channels="RGB", output_format="auto")
        st.write("---")
        df = pd.DataFrame({"col_1": ['Confidence Score Of Crash Happening In 1 Month',
                                     'Confidence Score Of Crash Happening In 3 Months',
                                     'Confidence Score Of Crash Happening In 6 Months'], "col_2": [0.0, 0.07, 0.8]},
                          index=['Confidence Score Of Crash Happening In 1 Month',
                                 'Confidence Score Of Crash Happening In 3 Months',
                                 'Confidence Score Of Crash Happening In 6 Months'])
        fig = px.bar(df["col_1"], y=df["col_2"], )
        st.plotly_chart(fig)
        st.write("Confidence score of prediction of a crash within the next month 1 interval: 0.0")
        st.write("Confidence score of prediction of a crash within the next month 3 interval: 0.07")
        st.write("Confidence score of prediction of a crash within the next month 6 interval: 0.8")
        st.write("---")
        if previous:
            image4 = Image.open(r"04-10(6) b.png")
            st.image(image4, caption="Crash predictor Performance for 2004-2010", width=None, use_column_width=None,
                     clamp=False,
                     channels="RGB", output_format="auto")
            image5 = Image.open(r"95-03(6) b.png")
            st.image(image5, caption="Crash predictor Performance for 1995-2003", width=None, use_column_width=None,
                     clamp=False,
                     channels="RGB", output_format="auto")
            image6 = Image.open(r"83-88(6) b.png")
            st.image(image6, caption="Crash predictor Performance for 1983-1988", width=None, use_column_width=None,
                     clamp=False,
                     channels="RGB", output_format="auto")
            image7 = Image.open(r"76-83(6) b.png")
            st.image(image7, caption="Crash predictor Performance for 1976-1983", width=None, use_column_width=None,
                     clamp=False,
                     channels="RGB", output_format="auto")
            image8 = Image.open(r"71-81(6) b.png")
            st.image(image8, caption="Crash predictor Performance 1971-1981", width=None, use_column_width=None,
                     clamp=False,
                     channels="RGB", output_format="auto")
        if details:
            st.header("Test Set Results:")
            st.write("Precision test (model/random):      0.06 / 0.02")
            st.write("Recall test (model/random):         0.62 / 0.21")
            st.write("Accuracy test (model/random):       0.8 / 0.78")
            st.write("Score test fbeta:                   0.23 / 0.08")

st.write('---')
