import os
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")
st.title("Live Math")

#upload your own work and math problem
question_col ,work_col = st.columns(2) 

with work_col:
    work = st.file_uploader("upload image of your work", key="work", type=['jpg', 'png', 'jpeg'])

with question_col:
    problem = st.file_uploader("upload image of question", key="problem" ,type=['jpg', 'png', 'jpeg'])

if st.button("display image"):
    if work and problem is not None:
        with work_col:    
            img = Image.open(work)
            st.image(img, width=500)
        with question_col:
            img2 = Image.open(problem)
            st.image(img2, width=500)
    else:
        st.write("Please upload image first:")

if st.button("clear chat"):
    st.session_state() = st.empty()