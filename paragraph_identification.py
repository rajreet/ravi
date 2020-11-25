import cv2
import copy
from preprocessing import showImage

def getText(process_dict, min_width=15, max_width=100):
    """
    Main function for paragraph identification
    """
    para_dict = process_dict
    
    para_dict["min_block_height"]=30

    block_stats = para_dict["block_stats"]
    para_dict["len_blockstat"] = len(block_stats)
    
    # para_dict["start_margin"]=5
    # para_dict["para_start"] = getLeftLine(para_dict,5)
    # para_dict["para_end"] = getRightLine(para_dict,5)

    # print(f"Paragraph start at X-coordinate : {para_dict['para_start']}")
    # print(f"Paragraph end at X-coordinate : {para_dict['para_end']}")
    
    # cv2.imwrite("cropped.png",process_dict["binary"][para_dict["top_page"]-10:para_dict["bottom_page"],para_dict["para_start"]-10:para_dict["para_end"]+10])
    return para_dict

def getParagraphs(process_dict):

    para_dict = getText(process_dict)
    return para_dict