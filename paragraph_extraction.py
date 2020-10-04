import os

def extract(para_dict):

    para_text=""
    for words in para_dict["tesseract_hocr_parsed"]:
        word_x0, word_y0, word_x1, word_y1 = words

        if(word_x0 >=para_dict["para_start"]-5):
            para_text+=para_dict["tesseract_hocr_parsed"][words]+" "

    file =open("output_para.txt","w")
    file.write(para_text)
    file.close()



