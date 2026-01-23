# executable.py

import time
import json
import os
from PIL import Image

from utils.ocr_utils import extract_ocr_data
from utils.field_extractors import (
    extract_dealer_name,
    extract_model_name,
    extract_horse_power,
    extract_asset_cost
)
from utils.vision_utils import detect_stamp_or_signature
from utils.signature_stamp import classify_stamp_signature
from utils.confidence import compute_confidence
from config import COST_PER_DOC_USD


def process_image(image_path, doc_id):
    start = time.time()

    image = Image.open(image_path)

    # ---------------- OCR ----------------
    ocr_data = extract_ocr_data(image)
    full_text = " ".join(ocr_data["text"])

    # ---------------- Field Extraction ----------------
    dealer = extract_dealer_name(full_text)
    model = extract_model_name(full_text)
    hp = extract_horse_power(full_text)
    cost = extract_asset_cost(full_text)

    # ---------------- Stamp / Signature ----------------
    present, bbox = detect_stamp_or_signature(image)

    image_width, image_height = image.size

    stamp_sig = classify_stamp_signature(
        bboxes=[bbox] if present else [],
        image_width=image_width,
        image_height=image_height
    )

    signature = stamp_sig["signature"]
    stamp = stamp_sig["stamp"]

    # ---------------- Output ----------------
    fields = {
        "dealer_name": dealer,
        "model_name": model,
        "horse_power": hp,
        "asset_cost": cost,
        "signature": signature,
        "stamp": stamp
    }

    return {
        "doc_id": doc_id,
        "fields": fields,
        "confidence": compute_confidence(fields),
        "processing_time_sec": round(time.time() - start, 2),
        "cost_estimate_usd": COST_PER_DOC_USD
    }


if __name__ == "__main__":
    DATASET_DIR = "dataset"
    results = []

    for file in os.listdir(DATASET_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(DATASET_DIR, file)
            print(f"Processing {file}...")
            result = process_image(img_path, file)
            results.append(result)

    os.makedirs("sample_output", exist_ok=True)

    with open("sample_output/result.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Processing complete. Results saved to sample_output/result.json")

