
import cv2 as cv
import os
from io import BytesIO
from langchain_groq import ChatGroq
import base64
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# This looks for the .env file and loads the variables
load_dotenv("data/.env")

grid_img = Image.open("maingrid.png")


#Process image uploads and canvas drawings
def processImage(img):
    try:
        
        #buffered = BytesIO()
        #img.save(buffered, format="JPEG")
        #img_str = base64.b64encode(buffered.getvalue())
        #if os.path.isfile(img):
            #with open(img, "rb") as file:
                #img_str = base64.b64encode(file.read()).decode("utf-8")
        #else:
            #print("Error: Path is a directory or does not exist.")
        img = Image.fromarray(img)
        buffered = BytesIO()
        img.save(buffered, format="PNG")    
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        #print(f"data:image/png;base64,{img_str}")
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"An error occurred in vision process: {e}")
        
            
def draw_img(image_base64:str, x_min:int, y_min:int, x_max:int, y_max:int, feedback_text:str):
    image_bytes = base64.b64decode(image_base64)
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([x_min,y_min,x_max,y_max], outline="red", width=4)
    draw.text((x_min,max(0, y_min)),feedback_text,fill="red")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")