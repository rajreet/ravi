import os
import subprocess
import copy

from pytesseract import pytesseract
from PIL import Image
import cv2
import numpy as np
import pandas as pd
from scipy.ndimage import interpolation as inter
from multiprocessing import Pool, Process, Pipe

from cropping import getLeftLine,getRightLine
from hocr_parse import parse_hocr
from cropping2 import getCropped 

from rlsa import rlsa



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

HORIZONTAL = (1, 0)
VERTICAL = (0, 1)

def showImage(winname, image, width=700, height=700):
    """
    Dsiplay the given image on screen, resized to specified dimensions

    Parameters:
        winname (str): window name

        image (cv::UMat): image to be displayed
    """
    cv2.imshow(winname, cv2.resize(image, (width, height)))
    cv2.waitKey(0)


def lineRemove(src, line_colour=WHITE):
    """
    Use morphology transformations for removing horizontal and vertical lines from image

    Parameters:
        src (image): source image
    Returns:
        src (image): updated image after line removal
    """
    # Transform source image to gray if it is not already
    if len(src.shape) != 2:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    else:
        gray = src

    # Apply adaptiveThreshold at the bitwise_not of gray, notice the ~ symbol
    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 15, -2)

    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)
    vertical = np.copy(bw)
    
    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols // 30

    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (horizontal_size, 1))

    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    #showImage("horizontal lines", horizontal)
    # Specify size on vertical axis
    rows = vertical.shape[0]
    verticalsize = rows // 30

    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, verticalsize))

    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    #showImage("vertical lines", vertical)
    contours_H, _ = cv2.findContours(
        horizontal, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_V, _ = cv2.findContours(
        vertical, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
    src = cv2.drawContours(src, contours_H, -1, line_colour, 3)
    src = cv2.drawContours(src, contours_V, -1, line_colour, 3)
    #showImage("final", src)
    return src

""" def correct_skew(image, delta=0.05, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray =  image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
              borderMode=cv2.BORDER_REPLICATE)

    return best_angle, rotated """

def get_rlsa_output(image, rlsa_param=30, type=HORIZONTAL):
    """
    Return inverted RLSA image, with intensity = rlsa_param

    Parameters:
        image (cv::UMat): image to be processed

        rlsa_param (int): threshold
    Returns:
        (cv::UMat): image after horizontal RLSA component connection
            and bitwise NOT operation
    """

    # im_height, im_width = image.shape[:2]
    # split = int(im_height/4)
    # part1,part2,part3,part4 = image[:split,:],image[split:split*2,:],image[2*split:split*3,:],image[3*split:,:]

    # parent_conn1, child_conn1 = Pipe()
    # parent_conn2, child_conn2 = Pipe()
    # parent_conn3, child_conn3 = Pipe()
    # parent_conn4, child_conn4 = Pipe()

    # p1 = Process(target=rlsa, args=(child_conn1,part1, True, False, 30)) 
    # p2 = Process(target=rlsa, args=(child_conn2,part2, True, False, 30,)) 
    # p3 = Process(target=rlsa, args=(child_conn3,part3, True, False, 30)) 
    # p4 = Process(target=rlsa, args=(child_conn4,part4, True, False, 30,)) 
  
    # p1.start() 
    # p2.start() 
    # p3.start() 
    # p4.start() 

    # outp1 = parent_conn1.recv()
    # outp2 = parent_conn2.recv()
    # outp3 = parent_conn3.recv()
    # outp4 = parent_conn4.recv()
    # # wait until process 1 is finished 
    # p1.join() 
    # # wait until process 2 is finished 
    # p2.join() 
    # # wait until process 3 is finished 
    # p3.join() 
    # # wait until process 4 is finished 
    # p4.join() 

    # concat = np.concatenate((outp1,outp2,outp3,outp4))

    concat = rlsa(image,True,False,30)
    # return inverted rlsa image
    return cv2.bitwise_not(concat)

def get_cca_output(image):
    """
    Function to return statitics of the rlsa based on connected component analysis

    Parameters:
        image (cv::UMat): image to be processed
    Returns:
        stats ():

        centroids ():
    """
    _, _, stats, centroids = cv2.connectedComponentsWithStats(image)
    return (stats, centroids)
    
def get_block_stats(stats, centroids):
    """
    Get block stats in a pandas DataFrams

    Parameters:
        stats ():

        centroids ():
    Returns:
        block_stats ():
    """
    stats_columns = ["left", "top", "width", "height", "area"]
    block_stats = pd.DataFrame(stats, columns=stats_columns)
    block_stats["centroid_x"], block_stats["centroid_y"] = centroids[:,
                                                                     0], centroids[:, 1]
    # Ignore the label 0 since it is the background
    block_stats.drop(0, inplace=True)
    return block_stats

def replaceColourBlocks(process_dict):
    """
    Replaces regions of binary image containing coloured heading boxes with light coloured
    text, with corresponding regions of inverse binary image

    Parameters:
        process_dict (dict): image processing data dictionary
    """

    binary_image = process_dict["binary"]

    inverse_bin = cv2.bitwise_not(binary_image)
    # showImage("inverse.png",inverse_bin)
    
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for each in contours:
        x, y, w, h = cv2.boundingRect(each)
        if 0.5 * process_dict["image_width"] < w < process_dict["image_width"] and h > 5:
            #print(x,y,w,h)
            binary_image[y: y+h, x: x+w] = inverse_bin[y: y+h, x: x+w]
            # showImage("conours", binary_image)

    process_dict["binary"] = lineRemove(binary_image)


def process(process_dict):
    replaceColourBlocks(process_dict)
    kernel = np.ones((2,2),np.uint8)
    opening = cv2.morphologyEx(cv2.bitwise_not(process_dict["binary"]), cv2.MORPH_OPEN, kernel)

    # cv2.imwrite("opening.png",cv2.bitwise_not(opening))

    process_dict["binary"]=cv2.bitwise_not(opening)
    cv2.imwrite("binary.png",process_dict["binary"])

    process_dict["page_rlsa"] = get_rlsa_output(copy.deepcopy(process_dict["binary"]))
    cv2.imwrite("rlsa.png",cv2.bitwise_not(process_dict["page_rlsa"]))

    process_dict["cropped"]=getCropped(process_dict)

    # stats, centroids = get_cca_output(process_dict["page_rlsa"])
    # block_stats = get_block_stats(stats, centroids)

    # block_stats["right"] = block_stats.left + block_stats.width
    # block_stats["bottom"] = block_stats.top + block_stats.height
    # process_dict["block_stats"] = block_stats

    # process_dict["top_page"]=10000000
    # process_dict["bottom_page"]=0
    # process_dict["min_block_height"]=30

    # process_dict["box"]=copy.deepcopy(process_dict["image"])
    # for i in range(len(block_stats)):
        
    #     if(150 > block_stats["height"].iloc[i]> process_dict["min_block_height"]):
    #         process_dict["top_page"]=min(process_dict["top_page"],block_stats["top"].iloc[i])
    #         process_dict["bottom_page"]=max(process_dict["bottom_page"],block_stats["bottom"].iloc[i])

    #         process_dict["box"]=cv2.rectangle(process_dict["box"],(block_stats["left"].iloc[i],block_stats["top"].iloc[i]),(block_stats["right"].iloc[i],block_stats["bottom"].iloc[i]),(0, 0, 0),thickness=2)
    #     # print(block_stats.iloc[i])


    # cv2.imwrite("rect.png",process_dict["box"])

    # process_dict["para_start"] = getLeftLine(process_dict,5)
    # process_dict["para_end"] = getRightLine(process_dict,5)

    # print(f"Paragraph start at X-coordinate : {process_dict['para_start']}")
    # print(f"Paragraph end at X-coordinate : {process_dict['para_end']}")
    
    # process_dict["cropped"]=process_dict["binary"][process_dict["top_page"]-10:process_dict["bottom_page"],process_dict["para_start"]-10:process_dict["para_end"]+10]

    cv2.imwrite("cropped.png",process_dict["cropped"])

    os.system("tesseract --dpi 300 cropped.png output_para")
    print("OCR Done")

    process_dict["tesseract_hocr_parsed"] = parse_hocr("output_text.hocr")
    
    return process_dict

def main():
    print("preprocessing....")

if __name__ == "__main__":
    main()