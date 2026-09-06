import streamlit as st
from PIL import Image
import src.vision
from src.logic import MathTutorEngine
from src.convo_hist import Conversation
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import streamlit.components.v1 as components
import gradio as gr
import json

#page_width = screeninfo.get_monitors.
st.set_page_config(layout="wide")
st.title("Live Math")
backgroundColor="#6E6D84"





Brain = MathTutorEngine()

if "Conversation_Class" not in st.session_state:
    st.session_state.Conversation_Class = Conversation()



#User uploads a screenshot of the math question they are working on and this section takes that image and returns latex for the llm to read.
with st.sidebar:
    st.header("Settings")
    
    problem = st.file_uploader("Upload Problem Image", type=['png', 'jpg', 'jpeg'])
    process_button=st.button("process image")
    text = st.text_area("write question")
    if process_button:
        if text is not None:
            
            st.session_state.Conversation_Class.add_system(text)
            
            open_question = Brain.get_opening_question(text) 
            st.session_state.Conversation_Class.add_ai(open_question)
            st.write(open_question)
                              
        else:
            #message for if images have not been uploaded
            st.write("Please upload image first:")


#Create and Initialize Streamlit Canvas
canvas_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: sans-serif;
            margin: 0;
            padding: 0;
        }
        #canvas-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        canvas {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            background-color: #ffffff;
            cursor: crosshair;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .toolbar {
            margin-top: 10px;
            display: flex;
            gap: 10px;
        }
        button {
            padding: 8px 16px;
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background-color: #ff2b2b;
        }
    </style>
</head>
<body>
    <div id="canvas-container">
        <canvas id="paintCanvas" width="600" height="400"></canvas>
        <div class="toolbar">
            <button onclick="clearCanvas()">Clear Canvas</button>
            <button onclick="sendDataToPython()">Get Data</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('paintCanvas');
        const ctx = canvas.getContext('2d');
        
        let painting = false;

        function getMousePos(canvas, evt) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: evt.clientX - rect.left,
                y: evt.clientY - rect.top
            };
        }

        function startPosition(e) {
            painting = true;
            draw(e);
        }

        function endPosition() {
            painting = false;
            ctx.beginPath();
        }

        function draw(e) {
            if (!painting) return;
            
            const pos = getMousePos(canvas, e);
            
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.strokeStyle = '#1f1f1f';

            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y);
        }

        canvas.addEventListener('mousedown', startPosition);
        canvas.addEventListener('mouseup', endPosition);
        canvas.addEventListener('mousemove', draw);

        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
        function sendDataToPython() {
            const dataURL = canvas.toDataURL('image/png');
    
            // This sends the data directly back to Python and triggers a script rerun
            window.streamlit.setComponentValue(dataURL);
        }
    </script>
</body>
</html>
"""

# Render the component in Streamlit
st.iframe(canvas_html, height=480)



#Main body of site
#User can send message to LLM, And this section handles the image data from the canvas and sends it to the Vision LLM to process.
with st.popover("Ask Question"):
    messages_container = st.container(height=400, border= True)
    user_question = st.text_area(
        "Ask AI Question",
        placeholder="e.g., 'Why should I...'"
    )
    
    if st.button("🛫"):
        #send image data to Vision.py
         
        if user_question is not None:
            question_prompt = {"messages": [{"role": "user", "content": f"User asked: {user_question}"}]}
            st.session_state.Conversation_Class.add_user(f"User asked: {user_question}")
            print(st.session_state.Conversation_Class.get_messages())
            response = Brain.ask(question_prompt)
            st.write(response)

with st.popover("Submit Work"):
    messages_container = st.container(height=400, border= True)
    reasoning = st.text_area(
        "Explain your reasoning (why did you write/draw this?):",
        placeholder="e.g., 'I identified these values from the problem statement...'"
    )
    
    if st.button("check work"):
        #send image data to Vision.py
        
         
        
        #prompt = {"messages": [{"role": "user", "content": f"User Submission: Reasoning:{reasoning} Canvas_Img_Data:{img_data}"}]}
        #st.session_state.Conversation_Class.add_user(f"User Submission: Reasoning:{reasoning} Canvas_Img_Data:{img_data}")
        #response = Brain.ask(prompt, img_data=user_drawing)
        messages_container.write(response)
            
                
        


