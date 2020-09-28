import pytesseract
from PIL import Image
import cv2
import numpy as np

file_path= "input\sample.jpg"
im = Image.open(file_path)
im.save("ocr.png", dpi=(300, 300))

image = cv2.imread("ocr.png",0)
image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
retval, threshold = cv2.threshold(image,180,255,cv2.THRESH_BINARY)

_ = cv2.imwrite("binary.png",threshold)