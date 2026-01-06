import app
import cv2 as cv
import numpy as np


def processImage(streamlit_img):
    if streamlit_img is None:
        return None

    img = np.array(streamlit_img).astype(np.uint8)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    #filtered_image = cv.bilateralFilter(gray_img, 10, 75, 75)
    thresh_img = cv.adaptiveThreshold(gray_img, 255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,199, 1)

    return thresh_img
    


