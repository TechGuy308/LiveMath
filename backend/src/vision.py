
import cv2 as cv
import os
from io import BytesIO
from langchain_groq import ChatGroq
import base64
from dotenv import load_dotenv
from PIL import Image

# This looks for the .env file and loads the variables
load_dotenv("data/.env")




#Process image uploads and canvas drawings (Takes PNG)
def processImage(img):
    try:
        if isinstance(img, (bytes, bytearray)):
            with Image.open(BytesIO(img)) as uploaded_image:
                img = uploaded_image.convert("RGBA")
        else:
            img = Image.fromarray(img)

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        #print(f"data:image/png;base64,{img_str}")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"An error occurred in vision process: {e}")
        
            
def draw_img(image_base64:str, x_min:int, y_min:int, x_max:int, y_max:int, feedback_text:str):
    
    pass