import cv2
from preprocessing import showImage

def getStartLine(para_dict,margin=10):
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

    


def getText(process_dict, min_width=15, max_width=100):
    """
    Main function for paragraph identification
    """
    para_dict = process_dict
    
    para_dict["min_block_height"]=30

    block_stats = para_dict["block_stats"]
    para_dict["len_blockstat"] = len(block_stats)
    
    para_dict["start_margin"]=5
    para_dict["para_start"] = getStartLine(para_dict,para_dict["start_margin"])

    print(f"Paragraph start at X-coordinate : {para_dict['para_start']}")
    
    # cv2.imwrite("line.png",cv2.line(process_dict['image'],(para_dict["para_start"],0),(para_dict["para_start"],para_dict["image_height"]),(0,0,0),2))
    return para_dict

def getParagraphs(process_dict):

    para_dict = getText(process_dict)
    return para_dict