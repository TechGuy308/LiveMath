import streamlit as st
from PIL import Image
import src.vision
from streamlit_drawable_canvas import st_canvas
from src.logic import MathTutorEngine
from streamlit_js_eval import streamlit_js_eval
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import streamlit.components.v1 as components

import json

#page_width = screeninfo.get_monitors.
st.set_page_config(layout="wide")
st.title("Live Math")
backgroundColor="#6E6D84"
chat_col, canvas_col = st.columns([1,3], border= True)

#To make canvas size responsive
page_width = streamlit_js_eval(
    js_expressions='screen.width',
    key='WIDTH'
    )
page_height = streamlit_js_eval(
    js_expressions='screen.height',
    key='HEIGHT'
    )
canvas_width = 1100
canvas_height = 600


if "quest_text" not in st.session_state:
    st.session_state.quest_text = None

if "user_work" not in st.session_state:
    st.session_state.user_work = None

@st.cache_resource
def load_tutor_engine():
    return MathTutorEngine()

if "engine" not in st.session_state:
    st.session_state.engine = load_tutor_engine()
    st.session_state.current_stage = 1
    st.session_state.current_question = None

if "ai_drawing" not in st.session_state:
    st.session_state.ai_drawing = []
#upload your math question



with st.sidebar:
    st.header("Settings")
    
    problem = st.file_uploader("Upload Problem Image", type=['png', 'jpg', 'jpeg'])
    process_button=st.button("process image")
    if process_button:
        if problem is not None:
            pil_quest_img = Image.open(problem)
            
            # 1. Get the LaTeX string from your vision script
            detected_text = src.vision.processImage(pil_quest_img, "text")
            #detected_text = r"\int\! x \, d_{X}"
            # 2. Save it to session state
            
            st.session_state["quest_text"] = detected_text
            
               
                    
        else:
            #message for if images have not been uploaded
            st.write("Please upload image first:")



with canvas_col:
    init_canvas =st_canvas(
        stroke_width=5,
        height=canvas_height, 
        width=canvas_width, 
        drawing_mode="freedraw", 
        key="canvas", 
        initial_drawing={"objects": st.session_state.ai_drawing}, 
        display_toolbar= True,
        update_streamlit=True)
    
    
with chat_col:
    messages_container = st.container(height=400, border= True)
    reasoning = st.text_area(
        "Explain your reasoning (why did you write/draw this?):",
        placeholder="e.g., 'I identified these values from the problem statement...'"
    )
    sumbit_button =     None
    if st.button("submit"):
        #send image data to Vision.py
        objects = init_canvas.json_data.get("objects")
            
        if objects:
            
            if init_canvas.json_data is not None:
                raw_objects = init_canvas.json_data.get("objects", [])
                analysis_results = src.vision.processImage(init_canvas.image_data, "formula")
                
                
            
        




#Call logic.py and Have the workflow between the user and ai setup
if st.session_state.quest_text:
    engine = st.session_state.engine
    
    # Get opening question
    if st.session_state.current_question is None:
        st.session_state.current_question = engine.get_opening_question(st.session_state["quest_text"])
    
    # Display
    with messages_container:
        st.progress(st.session_state.current_stage )
        st.write(st.session_state.current_question)
        
        
        
        if st.session_state.user_work:
            json_data = engine.validate_answer_with_feedback(st.session_state["quest_text"], st.session_state.current_question, reasoning, analysis_results)
            is_correct, hint, highlighter= engine.Ai_Interactions(json_data=json_data)
            if "CORRECT" in is_correct:
                st.success("✓ Correct!")
                
                # Save to memory
                engine.save_exchange(st.session_state.current_question, st.session_state.user_work)
                st.session_state.current_stage += 1
                st.session_state.current_question = engine.get_next_question(st.session_state["quest_text"])
                st.session_state.user_work = None
                st.rerun()
                
            else:
                    # Draw a red box on the canvas showing the mistake
                    st.session_state.ai_drawing.append(highlighter)
                
                    st.write(f"**Hint:** {hint}")
        
                    engine.save_exchange(st.session_state.current_question, st.session_state.user_work)
