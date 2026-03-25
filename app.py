import os
import streamlit as st
from PIL import Image
import src.vision
from streamlit_drawable_canvas import st_canvas
import src.logic

st.set_page_config(layout="wide")
st.title("Live Math")
backgroundColor="#6E6D84"
upload_problem_col, canvas_col = st.columns([1,1])

if "detected_latex" not in st.session_state:
    st.session_state.detected_latex = None

if "canvas_work" not in st.session_state:
    st.session_state.canvas_work = None

#upload your math question
with st.sidebar:
    st.header("Settings")
    problem = st.file_uploader("Upload Problem Image", type=['png', 'jpg', 'jpeg'])
    if st.button("process image"):
        if problem is not None:
            pil_quest_img = Image.open(problem)
            
            # 1. Get the LaTeX string from your vision script
            detected_text = src.vision.processImage(pil_quest_img)
            #detected_text = r"\int\! x \, d_{X}"
            # 2. Save it to session state
            with upload_problem_col:
                st.spinner("Ollama is thinking... (This takes a moment)")
            st.session_state["detected_latex"] = detected_text
            converted_latex = src.logic.solve_prob(detected_text)
            ollama_json = src.logic.get_steps(converted_latex[0], converted_latex[1])
                    
        else:
            #message for if images have not been uploaded
            st.write("Please upload image first:")

with canvas_col:
    init_canvas =st_canvas(
    "#090909",5, "#090909","#FDFCFC", height=170,width=400, drawing_mode="freedraw", key="canvas")
    if st.button("check work"):
         #detected_text = src.vision.processImage(init_canvas)
        canvas_text = r"\int\! x \, d_{X}"
        # 2. Save it to session state
        st.session_state["canvas_work"] = canvas_text
        



#display latex
if st.session_state["detected_latex"]:
    with upload_problem_col:
        st.write("---") # Visual separator
        st.write("### 🎯 Solve this problem:")
        st.latex(st.session_state["detected_latex"])