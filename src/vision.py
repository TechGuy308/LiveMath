
import cv2 as cv
import numpy as np
import os
from PIL import Image
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from io import BytesIO
import ollama
import moondream as md
from dotenv import load_dotenv

# This looks for the .env file and loads the variables
load_dotenv()
import pix2text
p2t = pix2text.Pix2Text.from_config()

# Now you can access them using os.environ
#my_api_key = os.getenv("API_KEY")
#model = md.vl(api_key=my_api_key)


#Process image uploads and canvas drawings
def processImage(streamlit_img, uploadType):
    if streamlit_img is None:
        return None
    else:
        
        if isinstance(streamlit_img, str) and streamlit_img.startswith("data:image"):
            import base64
            header, encoded = streamlit_img.split(",", 1)
            data = base64.b64decode(encoded)
            pil_img = Image.open(BytesIO(data)).convert("RGB")
            cv_img = cv.cvtColor(np.array(pil_img), cv.COLOR_RGB2BGR)
        else:
            # Standard file uploader image
            cv_img = np.array(streamlit_img).astype(np.uint8)
            pil_img = Image.fromarray(cv_img)
            #preps image to be more easily read

        try:
            #For the upload question
            if uploadType == "text":
                #Using pix2text for uploaded problems to retrieve text
                
                
                output = p2t.recognize(pil_img, file_type=uploadType)
                
                return output
            
            #For canvas 
            elif uploadType == "formula":
                #using moondream VLM for canvas, so that the ai can read it and then interact with it to a degree
                gray = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
                _, thresh = cv.threshold(gray, 230, 255, cv.THRESH_BINARY_INV)
                contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                
                detected_elements = []
                
                for i, cnt in enumerate(contours):
                    x, y, w, h = cv.boundingRect(cnt)
                    if w < 10 or h < 10: continue # Skip noise
                    
                    # Crop the element to identify it specifically
                    roi = pil_img.crop((x, y, x + w, y + h))
                    
                    # B. Use Pix2Text to see if it's an equation
                    math_out = p2t.recognize_formula(roi)
                    
                    detected_elements.append({
                        "id": i,
                        "box": [x, y, w, h],
                        "content": math_out if math_out else "drawing/arrow"
                    })

                # C. Use Moondream for Global Context (Step 3 in your Notebook)
                buffered = BytesIO()
                pil_img.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()

                response = ollama.generate(
                    model='moondream',
                    prompt='''Describe this physics sketch. 
                    Identify arrows and their directions. 
                    Identify objects like blocks or ramps. 
                    Keep it concise.''',
                    images=[img_bytes]
                )
                
                # Package for Logic.py
                final_payload = {
                    "spatial_description": response['response'],
                    "elements": detected_elements
                }
                return final_payload
                
        except Exception as e:
            print(f"An error occurred: {e}")
        
            
