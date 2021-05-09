from rlsa import rlsa
import cv2
import pandas as pd
import copy

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

def getCropped(process_dict):
    image = process_dict['page_rlsa']

    rlsa_vertical=rlsa(cv2.bitwise_not(image),False,True,40)

    cv2.imwrite("rlsa_vertical.png",rlsa_vertical)

    _, _, stats, centroids = cv2.connectedComponentsWithStats(cv2.bitwise_not(rlsa_vertical))

    block_stats = get_block_stats(stats, centroids)

    block_stats["right"] = block_stats.left + block_stats.width
    block_stats["bottom"] = block_stats.top + block_stats.height

    box=copy.deepcopy(rlsa_vertical)

    max_area=0
    cropped_top,cropped_bottom,cropped_left,cropped_right = 0,0,0,0

    for i in range(len(block_stats)):
        top = block_stats["top"].iloc[i]
        bottom=block_stats["top"].iloc[i]+block_stats["height"].iloc[i]
        left=block_stats["left"].iloc[i]
        right=block_stats["left"].iloc[i]+block_stats["width"].iloc[i]

        if(int(block_stats["height"].iloc[i])*int(block_stats["width"].iloc[i]) > max_area and\
             block_stats["width"].iloc[i] < process_dict['image_width']-10):

            cropped_top=top
            cropped_bottom=bottom
            cropped_left=left
            cropped_right=right

            max_area=int(block_stats["height"].iloc[i])*int(block_stats["width"].iloc[i])

        # box=cv2.rectangle(box,(left,top,right,bottom),(0, 0, 255),thickness=2)

    box=cv2.rectangle(box,(cropped_left,cropped_top),(cropped_right,cropped_bottom),(0, 0, 0),thickness=4)

    cv2.imwrite("rlsa_rect.png",box)

    return process_dict["binary"][cropped_top:cropped_bottom,cropped_left:cropped_right]