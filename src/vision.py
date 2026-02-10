import app
import cv2 as cv
import numpy as np
import easyocr 


reader = easyocr.Reader(['en'])
def processImage(streamlit_img):
    if streamlit_img is None:
        return None
    else:
        
        img = np.array(streamlit_img).astype(np.uint8)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
        resized_img=cv.resize(gray_img,None,None,7,7, interpolation=cv.INTER_CUBIC)
        
        thresh_img = cv.adaptiveThreshold(resized_img, 255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,199, 1)
        result = reader.readtext(resized_img)
        for(bbox, text, prob) in result:
            print(text)
        
        return(resized_img)
            
     
    


