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
import streamlit_excalidraw

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
canvas_width = page_width 
canvas_height = page_height

#Creates grid for Streamlit Canvas
fig, axis = plt.subplots()
axis.grid(True)
axis.set_xlim(0, canvas_width)
axis.set_ylim(0, canvas_height)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
buf = io.BytesIO()

folder = 'src'
filename = 'grid.png'
# Combine path and save
full_path = os.path.join(folder, filename)

plt.savefig(buf, format='png')
buf.seek(0)
grid = Image.open(buf)


img_str = base64.b64encode(buf.read()).decode()
grid_url = f"data:image/png;base64,{img_str}"
plt.close()



if "quest_text" not in st.session_state:
    st.session_state.quest_text = None

if "user_work" not in st.session_state:
    st.session_state.user_work = None

if "engine" not in st.session_state:
    st.session_state.engine = MathTutorEngine()
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
        update_streamlit=False)
    export_data = streamlit_excalidraw.excalidraw_whiteboard(height=600, key="my_canvas", trigger_export=True)
    
with chat_col:
    messages_container = st.container(height=400, border= True)
    reasoning = st.text_area(
        "Explain your reasoning (why did you write/draw this?):",
        placeholder="e.g., 'I identified these values from the problem statement...'"
    )
        
    if st.button("submit"):
        st.write(str(export_data) + "hi")
         #detected_text = src.vision.processImage(init_canvas)
        if export_data is not None:
            
            objects = init_canvas.json_data.get("objects")
            
            
            if objects:
                analysis_results = src.vision.processImage(init_canvas.image_data, "formula")
                # 2. Save it to session state
                st.session_state.user_work = {
                "visual_analysis": analysis_results, 
                "reasoning": reasoning
            }
                st.rerun()
            else:
                st.warning("Please Draw Something")
    
        




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
            # Validate
            if engine.validate_answer(st.session_state["quest_text"], st.session_state.current_question, st.session_state.user_work):
                st.success("✓ Correct!")
                
                # Save to memory
                engine.save_exchange(st.session_state.current_question, st.session_state.user_work)
                st.session_state.current_stage += 1
                st.session_state.current_question = engine.get_next_question(st.session_state["quest_text"])
                st.session_state.user_work = None
                st.rerun()
                # Check if done
                '''if engine.check_problem_complete(st.session_state["quest_text"]):
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
                    st.rerun()'''
            else:

                st.session_state.ai_drawing.append(engine.Ai_Draw)
                st.error("❌ Not correct. Try again.")
                engine.save_exchange(st.session_state.current_question, st.session_state.user_work)
