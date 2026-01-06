import os
import streamlit as st
from PIL import Image
import src.vision

st.set_page_config(layout="wide")
st.title("Live Math")

counter = 0

if "counter" not in st.session_state:
    st.session_state["counter"] = 0

if st.button("counter"):
    
    st.session_state["counter"] += 1

st.write(st.session_state["counter"])
