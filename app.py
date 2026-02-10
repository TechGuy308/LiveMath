import os
import streamlit as st
from PIL import Image
import src.vision

st.set_page_config(layout="wide")
st.title("Live Math")

#upload your own work and math problem
question_col ,work_col = st.columns(2) 

with work_col:
    work = st.file_uploader("upload image of your work", key="work", type=['jpg', 'png', 'jpeg'])

with question_col:
    problem = st.file_uploader("upload image of question", key="problem" ,type=['jpg', 'png', 'jpeg'])

#initilize session state
if "work_img" not in st.session_state:
    st.session_state["work_img"] = None
if "quest_img" not in st.session_state:
    st.session_state["quest_img"] = None

#display image
if st.button("display image"):
    #check to see that work and problem images have been uploaded
    if work and problem is not None:
        with work_col:  
            pil_work_img = Image.open(work)
            st.session_state["work_img"] = src.vision.processImage(pil_work_img)
            st.image(st.session_state["work_img"], 300)
            

        with question_col:
            pil_quest_img = Image.open(problem)
            st.session_state["quest_img"] = src.vision.processImage(pil_quest_img)
            st.image(st.session_state["quest_img"], 300)
            
    else:
        #message for if images have not been uploaded
        st.write("Please upload image first:")


if st.button("clear chat"):
    st.session_state["work_img"] = None
    st.session_state["quest_img"] = None