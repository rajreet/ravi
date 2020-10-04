import pytesseract
from PIL import Image
import cv2
import numpy as np
from preprocessing import process
from paragraph_identification import getParagraphs
from paragraph_extraction import extract

def main():
    
    process_dict={}
    image = cv2.imread("input\sample.jpg",cv2.IMREAD_IGNORE_ORIENTATION)
    # cv2.imwrite('ocr.png',image)

    process_dict["image"]=image
    process_dict["image_height"] = image.shape[0]
    # print(process_dict["image_height"])
    process_dict["image_width"] = image.shape[1]
    retval, threshold = cv2.threshold(image,150,255,cv2.THRESH_BINARY)
    # cv2.imwrite("binary.png",threshold)

    process_dict["binary"]=threshold


    process_dict=process(process_dict)
    print("Image preprocssing done.")
    para_dict = getParagraphs(process_dict)
    extract(para_dict)

    # showImage("binary.png",process_dict["binary"])

if __name__ == "__main__":
    main()