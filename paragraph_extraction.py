import os

def extract(para_dict):

    para_text=""
    whole_text=""

    block_stats = para_dict["block_stats"]

    for i in range(len(block_stats)):

        if(block_stats["height"].iloc[i] > 20 and i):

            for words in para_dict["tesseract_hocr_parsed"]:
                word_x0, word_y0, word_x1, word_y1 = words

                left=block_stats["left"].iloc[i]
                right=block_stats["right"].iloc[i]
                top=block_stats["top"].iloc[i]
                bottom= block_stats["bottom"].iloc[i]

                if(word_x0 >=left-10 and word_x1 <= right+10 and word_y0 >= top-10 and word_y1 <= bottom +10):
                    para_text+=para_dict["tesseract_hocr_parsed"][words]+" "


            # print(para_text)
            # print(f"{left} {top} {right} {bottom}")

            whole_text+=para_text
            para_text=""

    file =open("output_para.txt","w")
    file.write(whole_text)
    file.close()



