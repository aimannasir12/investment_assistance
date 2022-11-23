import streamlit as st
st.set_page_config(page_title="Feel Free To Suggest Improvements,page_icon="✉️"")
st.header(":mailbox: Get In Touch With Us!")
st.write("We Are Eager To Help With Relevant Queries And Look Forward To Your Suggestions.:smile:")
page_bg_img1="""
<style>
[data-testid="stAppViewContainer"]{
background-image:url("https://media.istockphoto.com/photos/an-organised-workspace-leads-to-more-productivity-picture-id1305990690?b=1&k=20&m=1305990690&s=170667a&w=0&h=MxoLf1JAmPQOQ7YYDg_AVfA4eiK9n9OMB8o3mNNYJJM=");
background-size: cover;}
</style>
"""
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
st.markdown(page_bg_img1,unsafe_allow_html=True)
contact_form="""
<form action="https://formsubmit.co/machinelearningisfun12@gmail.com" method="POST">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>"""
st.markdown(contact_form,unsafe_allow_html=True)
how="""
<style>
input[type=text], input[type=email], textarea {
  width: 100%; 
  padding: 12px; 
  border: 1px solid 
  border-radius: 4px; 
  box-sizing: border-box; 
  margin-top: 6px; 
  margin-bottom: 16px; 
  resize: vertical 
}
button[type=submit]:hover {
  background-color: #45a049;
}
</style>
"""
st.markdown(how, unsafe_allow_html=True)
