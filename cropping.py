def getLeftLine(process_dict,delta=10,margin=10):
    block_stats = process_dict["block_stats"]

    start=delta

    maxcount=0
    maxstart=start

    while(start<process_dict["image_width"]-50):
        count=0

        for i in range(len(block_stats)):
            if(start<=block_stats["left"].iloc[i] <=start+margin and block_stats["height"].iloc[i]>process_dict["min_block_height"]):
                count+=1

        if(maxcount<count):
            maxcount=count
            maxstart=start
        
        start+=delta

    return maxstart

def getRightLine(process_dict,delta=10,margin=10):
    block_stats = process_dict["block_stats"]

    start=process_dict["image_width"]

    maxcount=0
    maxstart=start

    while(start>process_dict["para_start"]):
        count=0

        for i in range(len(block_stats)):
            if(start>=block_stats["right"].iloc[i] >=start-margin and block_stats["height"].iloc[i]>process_dict["min_block_height"]):
                count+=1

        if(maxcount<count):
            maxcount=count
            maxstart=start
        
        start-=delta

    return maxstart
