import os
import streamlit as st
from PIL import Image
import src.vision
from streamlit_drawable_canvas import st_canvas
from src.logic import MathTutorEngine
import asyncio

st.set_page_config(layout="wide")
st.title("Live Math")
backgroundColor="#6E6D84"
upload_problem_col, canvas_col = st.columns([1,1])

if "quest_text" not in st.session_state:
    st.session_state.quest_text = None

if "user_work" not in st.session_state:
    st.session_state.user_work = None

if "engine" not in st.session_state:
    st.session_state.engine = MathTutorEngine()
    st.session_state.current_stage = 1
    st.session_state.current_question = None

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
    "#090909",5, "#090909","#FDFCFC", height=400,width=400, drawing_mode="freedraw", key="canvas")
    user_text_input = st.text_area("Enter your reasoning or questions")
    
    if st.button("submit"):
         #detected_text = src.vision.processImage(init_canvas)
        canvas_latex = src.vision.processImage(init_canvas.image_data, "formula")
        # 2. Save it to session state
        st.session_state.user_work = f"user's question/explanation:{user_text_input}. The Equation they wrote:{str(canvas_latex)}"
    
        



#display latex


#Call logic.py and Have the workflow between the user and ai setup
if st.session_state.quest_text:
    engine = st.session_state.engine
    
    # Get opening question
    if st.session_state.current_question is None:
        st.session_state.current_question = engine.get_opening_question(st.session_state["quest_text"])
    
    # Display
    with upload_problem_col:
        st.write(f"### Stage {st.session_state.current_stage}")
        st.write(st.session_state.current_question)
        
        
        
        if st.session_state.user_work:
            # Validate
            if engine.validate_answer(st.session_state["quest_text"], st.session_state.current_question, st.session_state.user_work):
                st.success("✓ Correct!")
                
                # Save to memory
                engine.save_exchange(st.session_state.current_question, st.session_state.user_work)
                
                # Check if done
                if engine.check_problem_complete(st.session_state["quest_text"]):
                    st.balloons()
                    st.success("🎉 Problem Complete!")
                    
                    if st.button("New Problem"):
                        engine.reset()
                        st.session_state.current_stage = 1
                        st.session_state.current_question = None
                        st.rerun()
                else:
                    # Get next question
                    st.session_state.current_stage += 1
                    st.session_state.current_question = engine.get_next_question(st.session_state["quest_text"])
                    st.rerun()
            else:
                st.error("❌ Not correct. Try again.")