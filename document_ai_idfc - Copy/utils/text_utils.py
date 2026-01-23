# utils/text_utils.py

import re

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_numbers(text):
    return re.findall(r'\d+', text)
