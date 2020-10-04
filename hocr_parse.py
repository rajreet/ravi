from collections import OrderedDict
import bs4 as bs


def parse_hocr(hocr_file):
	"""
	Uses BeautifulSoup to extract data from hocr file into an ordered dictionary

	Parameters:
		hocr_file (.hocr): file created by tesseract
	Returns:
		result (OrderedDict): ordered dictionary containing co-ordinates as keys
			and data as values
	"""
	# Make sure we got a HOCR file handle when called
	if not hocr_file:
		raise ValueError("The parser must be provided with an HOCR file handle.")
	
	# Open the hocr file, read it into BeautifulSoup and extract all the ocr words
	hocr = open(hocr_file,"r",encoding='utf8').read()
	soup = bs.BeautifulSoup(hocr,"html.parser")
	words = soup.find_all("span",class_="ocrx_word")
	result = OrderedDict()
	
	# Loop through all the words and look for our search terms
	for word in words:
		w = word.get_text()
		bbox = word["title"].split(";")
		bbox = bbox[0].split(" ")
		bbox = tuple([int(x) for x in bbox[1:]])
		result[bbox] = w
	
	return result
