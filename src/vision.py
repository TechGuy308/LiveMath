import app
import cv2 as cv
import numpy as np
import easyocr 
import os
from PIL import Image




def processImage(streamlit_img):
    if streamlit_img is None:
        return None
    else:
        #preps image to be more easily read
        img = np.array(streamlit_img).astype(np.uint8)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
        resized_img=cv.resize(gray_img,None,None,7,7, interpolation=cv.INTER_CUBIC)
        thresh_img = cv.adaptiveThreshold(resized_img, 255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,199, 1)
        
        # Convert numpy array back to PIL Image for pix2text
        resized_pil = Image.fromarray(thresh_img)
        
        #creates file in which latex output is stored(temporary)
        file_path = 'my_new_file.txt'
        content_to_write = "Hello, world!\nThis is a new text file created with Python.\n"

        try:
            #reads image and converts forumla to latex
            import pix2text
            p2t = pix2text.Pix2Text.from_config()
            output = p2t.recognize(resized_pil, file_type="text")

            #writes latex output to file and then returns output so it can be displayed in app.py 
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(output)
            print(f"File '{file_path}' created and written successfully.")
            return output
        except Exception as e:
            print(f"An error occurred: {e}")
        
            
     
    


