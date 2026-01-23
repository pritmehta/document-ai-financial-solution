# utils/field_extractors.py

import pandas as pd
import re
from rapidfuzz import process, fuzz

# -------------------------------------------------------------------
# Load master data safely
# -------------------------------------------------------------------

try:
    dealer_df = pd.read_csv("data/master_data/dealer_master.csv")
    DEALER_LIST = dealer_df["dealer_name"].dropna().tolist()
except Exception:
    DEALER_LIST = []

try:
    model_df = pd.read_csv("data/master_data/model_master.csv")
    MODEL_LIST = model_df["model_name"].dropna().tolist()
except Exception:
    MODEL_LIST = []


# -------------------------------------------------------------------
# Helper: normalize text for fuzzy matching
# -------------------------------------------------------------------

def normalize_text(text):
    """
    Normalize text to make fuzzy matching robust
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text)          # collapse spaces
    return text.strip()


# -------------------------------------------------------------------
# Dealer Name Extraction (ROBUST, MULTI-LINE)
# -------------------------------------------------------------------

def extract_dealer_name(ocr_text):
    """
    Extract dealer name using multi-line fuzzy matching
    """
    if not DEALER_LIST:
        return None

    # Normalize dealer master
    normalized_dealers = {
        normalize_text(d): d for d in DEALER_LIST
    }

    # Normalize OCR lines
    lines = [
        normalize_text(l)
        for l in ocr_text.split("\n")
        if len(l.strip()) > 2
    ]

    best_match = None
    best_score = 0

    # Sliding window over OCR lines
    for i in range(len(lines)):
        for window in range(3, 7):
            chunk = " ".join(lines[i:i + window])
            if not chunk:
                continue

            match = process.extractOne(
                chunk,
                normalized_dealers.keys(),
                scorer=fuzz.partial_ratio
            )

            if match:
                score = match[1]
                if score > best_score:
                    best_score = score
                    best_match = normalized_dealers[match[0]]

    return best_match if best_score >= 75 else None


# -------------------------------------------------------------------
# Model Name Extraction (MASTER-BASED)
# -------------------------------------------------------------------

def extract_model_name(ocr_text):
    """
    Extract model name using normalized exact containment
    """
    text = ocr_text.upper().replace(" ", "").replace("-", "")

    for model in MODEL_LIST:
        m = model.upper().replace(" ", "").replace("-", "")
        if m in text:
            return model

    return None


# -------------------------------------------------------------------
# Horse Power Extraction (SAFE RANGE)
# -------------------------------------------------------------------

def extract_horse_power(ocr_text):
    """
    Extract tractor HP (valid range filtering)
    """
    candidates = re.findall(
        r"(\d{2,3})\s*(?:HP|H\.P|HORSE\s*POWER)",
        ocr_text,
        re.IGNORECASE
    )

    candidates = [
        int(c) for c in candidates
        if 20 <= int(c) <= 80
    ]

    return candidates[0] if candidates else None


# -------------------------------------------------------------------
# Asset Cost Extraction (CONTEXT-AWARE)
# -------------------------------------------------------------------

def extract_asset_cost(ocr_text):
    """
    Extract total / full cost of tractor robustly
    """
    lines = ocr_text.split("\n")

    # Priority 1: lines with explicit cost keywords
    for line in lines:
        if any(k in line.lower() for k in ["total", "full cost", "total rs"]):
            nums = re.findall(r"\b\d{5,7}\b", line.replace(",", ""))
            nums = [
                int(n) for n in nums
                if 200000 <= int(n) <= 2000000
            ]
            if nums:
                return max(nums)

    # Priority 2: fallback within reasonable tractor price range
    nums = re.findall(r"\b\d{5,7}\b", ocr_text.replace(",", ""))
    nums = [
        int(n) for n in nums
        if 200000 <= int(n) <= 2000000
    ]

    return max(nums) if nums else None
