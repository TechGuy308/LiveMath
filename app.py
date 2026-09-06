from PIL import Image

from src.logic import MathTutorEngine
from src.convo_hist import Conversation
import gradio as gr


Brain = MathTutorEngine()
History = Conversation()

demo = gr.Interface(fn=Brain.vision, inputs=gr.ImageEditor(type="numpy", sources=(), brush=gr.Brush(colors=["#000000"])), outputs="text")
demo.launch()