import cv2
import copy
from preprocessing import showImage

def getLeftLine(para_dict,margin=10):
    block_stats = para_dict["block_stats"]

    start=margin

    maxcount=0
    maxstart=start

    while(start<para_dict["image_width"]-50):
        count=0

        for i in range(len(block_stats)):
            if(start<=block_stats["left"].iloc[i] <=start+margin and block_stats["height"].iloc[i]>para_dict["min_block_height"]):
                count+=1

        if(maxcount<count):
            maxcount=count
            maxstart=start
        
        start+=margin

    return maxstart

def getRightLine(para_dict,margin=10):
    block_stats = para_dict["block_stats"]

    start=para_dict["image_width"]

    maxcount=0
    maxstart=start

    while(start>para_dict["para_start"]):
        count=0

        for i in range(len(block_stats)):
            if(start>=block_stats["right"].iloc[i] >=start-margin and block_stats["height"].iloc[i]>para_dict["min_block_height"]):
                count+=1

        if(maxcount<count):
            maxcount=count
            maxstart=start
        
        start-=margin

    return maxstart

    


def getText(process_dict, min_width=15, max_width=100):
    """
    Main function for paragraph identification
    """
    para_dict = process_dict
    
    para_dict["min_block_height"]=30

    block_stats = para_dict["block_stats"]
    para_dict["len_blockstat"] = len(block_stats)
    
    # para_dict["start_margin"]=5
    para_dict["para_start"] = getLeftLine(para_dict,5)
    para_dict["para_end"] = getRightLine(para_dict,5)

    print(f"Paragraph start at X-coordinate : {para_dict['para_start']}")
    print(f"Paragraph end at X-coordinate : {para_dict['para_end']}")
    
    process_dict["crop_lines"]=copy.deepcopy(process_dict["image"])

    process_dict["crop_lines"]=cv2.line(process_dict['crop_lines'],(para_dict["para_start"],0),(para_dict["para_start"],para_dict["image_height"]),(0,0,0),2)
    process_dict["crop_lines"]=cv2.line(process_dict['crop_lines'],(para_dict["para_end"],0),(para_dict["para_end"],para_dict["image_height"]),(0,0,0),2)
    process_dict["crop_lines"]=cv2.line(process_dict['crop_lines'],(0,para_dict["top_page"]),(para_dict["image_width"],para_dict["top_page"]),(0,0,0),2)
    process_dict["crop_lines"]=cv2.line(process_dict['crop_lines'],(0,para_dict["bottom_page"]),(para_dict["image_width"],para_dict["bottom_page"]),(0,0,0),2)

    cv2.imwrite("line.png",process_dict["crop_lines"])
    cv2.imwrite("cropped.png",process_dict["binary"][para_dict["top_page"]-10:para_dict["bottom_page"],para_dict["para_start"]-10:para_dict["para_end"]+10])
    return para_dict

def getParagraphs(process_dict):

    para_dict = getText(process_dict)
    return para_dict