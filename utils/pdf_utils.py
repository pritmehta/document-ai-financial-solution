# utils/pdf_utils.py

from pdf2image import convert_from_path

def pdf_to_images(pdf_path):
    """
    Converts PDF to list of PIL Images
    """
    images = convert_from_path(pdf_path, dpi=300)
    return images
