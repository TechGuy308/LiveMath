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

if "work_img" not in st.session_state:
    st.session_state["work_img"] = None
if "quest_img" not in st.session_state:
    st.session_state["quest_img"] = None

if st.button("display image"):
    if work and problem is not None:
        with work_col:    
            st.session_state["work_img"] = Image.open(work)
            st.image(st.session_state["work_img"], 300)

        with question_col:
            st.session_state["quest_img"] = Image.open(problem)
            st.image(st.session_state["quest_img"], 300)
            
    else:
        st.write("Please upload image first:")

if st.button("clear chat"):
    st.session_state["work_img"] = None
    st.session_state["quest_img"] = None