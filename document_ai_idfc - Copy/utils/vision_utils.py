# utils/vision_utils.py

import cv2
import numpy as np

def detect_stamp_or_signature(image):
    """
    Simple heuristic-based detection
    Returns (present, bbox)
    """
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 5000:
            return True, [x, y, x + w, y + h]

    return False, None
