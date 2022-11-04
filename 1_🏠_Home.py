import streamlit as st
page_bg_img="""
<style>
[data-testid="stAppViewContainer"]{
background-image:url("https://media.istockphoto.com/photos/various-of-international-money-coin-and-banknote-background-time-picture-id1019220022?b=1&k=20&m=1019220022&s=170667a&w=0&h=pjXL7NmGGKa2F4PeePBImIGPG0eNAFEqlKaSFILWCJ4=");
background-size: cover;}
</style>
"""
st.set_page_config(page_title="Welcome to our Small Investor Advisor", page_icon="🏠")
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
st.markdown(page_bg_img,unsafe_allow_html=True)
main_title = '<p style="font-family:Fantasy; color:Black; font-size: 85px;">INVESTOR ADVISOR </p>'
st.markdown(main_title,unsafe_allow_html=True)
st.write("---")
main_title2 = '<p style="font-family:Monospace; color:Black; font-size: 20px;">Welcome To Our Investment Advisor/Assistant!!...An App That Solves Your Doubts Related To Investing With The Help Of Machine Learning.</p>'
st.markdown(main_title2,unsafe_allow_html=True)
col1, col2= st.columns(2)

with col1:
    sub_title1 = '<p style="font-family:Times New Roman; color:Black; font-size: 40px;">1.Stock Price Prediction</p>'
    st.markdown(sub_title1, unsafe_allow_html=True)
    sub_title1a = '<p style="font-family:Monospace; color:Black; font-size: 20px;">Visualise The Predicted Price Of A Stock Based On Factors Such As The Financial Performance Of The Company Over A Period Of Your Choice.</p>'
    st.markdown(sub_title1a, unsafe_allow_html=True)
    sub_title2 = '<p style="font-family:Times New Roman; color:Black; font-size: 40px;">2.Current Market Psychology</p>'
    st.markdown(sub_title2, unsafe_allow_html=True)
    sub_title2a = '<p style="font-family:Monospace; color:Black; font-size: 20px;">Get An Insight Into The Minds Behind Based On What They Are Discussing About The Market.</p>'
    st.markdown(sub_title2a, unsafe_allow_html=True)
with col2:
    sub_title3 = '<p style="font-family:Times New Roman; color:Black; font-size: 40px;">3.Financial Expert Sentiments</p>'
    st.markdown(sub_title3, unsafe_allow_html=True)
    sub_title3a = '<p style="font-family:Monospace; color:Black; font-size: 20px;">Get All The Financial News Compiled In One Place To Get An Overall View Of Expert Market Perception.</p>'
    st.markdown(sub_title3a, unsafe_allow_html=True)
    sub_title4 = '<p style="font-family:Times New Roman; color:Black; font-size: 40px;">4.Portfolio Recommendation</p>'
    st.markdown(sub_title4, unsafe_allow_html=True)
    sub_title4a = '<p style="font-family:Monospace; color:Black; font-size: 20px;">Get A Sense Of Where To Allocate Your Stocks Based on Your Needs And Risk Vs Returns.</p>'
    st.markdown(sub_title4a, unsafe_allow_html=True)
st.write("---")
#bottom_title = '<p style="font-family:Times New Roman; color:Black; font-size: 20px;">Please Use The Navigation Bar On The Left To Access These Features</p>'
st.write(":information_source:   Please Use The Navigation Bar On The Left To Access These Features.")
#st.markdown(bottom_title, unsafe_allow_html=True)
