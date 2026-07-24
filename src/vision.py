
import cv2 as cv
import numpy as np
import os
from PIL import Image
import src.prompts as prompts
from langchain_core.prompts import ChatPromptTemplate
from io import BytesIO
import ollama


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
       
            # 1. Convert NumPy array directly to PIL RGBA image
        
                        
        try:
            #For the upload question
            if uploadType == "text":
                #Using pix2text for uploaded problems to retrieve text
                output = p2t.recognize(streamlit_img, file_type=uploadType)
                return output
            
            #For canvas 
            elif uploadType == "formula":
                raw_pil = Image.fromarray(streamlit_img.astype('uint8'), 'RGBA')
                            
                            # 2. Create a solid white background image of the same size
                white_bg = Image.new("RGBA", raw_pil.size, (255, 255, 255, 255))
                            
                            # 3. Composite the drawing on top of the white background
                            # (This strips transparency cleanly without turning the background black!)
                pil_img = Image.alpha_composite(white_bg, raw_pil).convert("RGB")
                            
                        # Handle normal uploaded file objects (from st.file_uploader)

                cv_img = cv.cvtColor(np.array(pil_img), cv.COLOR_RGB2BGR)
                gray = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
                _, thresh = cv.threshold(gray, 230, 255, cv.THRESH_BINARY_INV)
                
                
                cv.imwrite("debug_contours.png", thresh)
                
                #math_out = p2t.recognize_formula(roi)

                
                buffered = BytesIO()
                pil_img.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()

                response = ollama.generate(
                  model="qwen2.5vl",
                  prompt= prompts.VISION_LLM_PROMPT,
                  images=[img_bytes]
                )
                
                # Package for Logic.py
                print(response.response)
                return response.response
                
        except Exception as e:
            print(f"An error occurred: {e}")
        
            
