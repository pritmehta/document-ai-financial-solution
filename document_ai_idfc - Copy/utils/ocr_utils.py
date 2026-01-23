# utils/ocr_utils.py

import pytesseract
from pytesseract import Output
from config import TESSERACT_LANGS

# Explicit path to Tesseract executable (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_ocr_data(image):
    """
    Returns OCR text + bounding boxes
    """
    data = pytesseract.image_to_data(
        image,
        lang=TESSERACT_LANGS,
        output_type=Output.DICT
    )
    return data

