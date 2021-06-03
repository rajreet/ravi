import pytesseract
from PIL import Image
import cv2
import numpy as np
from preprocessing import process
from paragraph_identification import getParagraphs
from paragraph_extraction import extract

import time

def main():
    
    for image_count in range(1,6):

        process_dict={}
        image = cv2.imread(f"input/{image_count}.jpg",cv2.IMREAD_GRAYSCALE)
        # cv2.imwrite('ocr.png',image)

        # if (image.shape[0] < image.shape[1]):
        #     image = 
        
        process_dict["image"]=image
        process_dict["image_height"] = image.shape[0]
        process_dict["image_width"] = image.shape[1]
        # retval, thresh = cv2.threshold(image,200,255,cv2.THRESH_BINARY)

        print(image.shape)
        # cv2.imwrite("thresh_200.png",thresh)

        threshold = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,201,15)
        # blur = cv2.GaussianBlur(image,(7,7),0)
        # retval, threshold = cv2.threshold(blur,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        process_dict["binary"]=threshold

        process_dict["count"]=image_count

        process_dict=process(process_dict)
        print(f"Image preprocessing done for {image_count}.")
        # para_dict = getParagraphs(process_dict)
        # extract(para_dict)

        # showImage("binary.png",process_dict["binary"])

if __name__ == "__main__":
    start_time = time.time()
    main()
    print()
    print("============================== Runtime Elapsed =======================================")
    print(f"{time.time()-start_time} Seconds")
    print("======================================================================================")