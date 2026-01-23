# utils/signature_stamp.py

def classify_stamp_signature(bboxes, image_width, image_height):
    """
    Separate stamp and signature using spatial heuristics.

    Heuristic:
    - Signature: bottom-right quadrant
    - Stamp: elsewhere
    """

    signature_box = None
    stamp_box = None

    for box in bboxes:
        x1, y1, x2, y2 = box
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Bottom-right → signature
        if cx > image_width * 0.55 and cy > image_height * 0.55:
            signature_box = box
        else:
            stamp_box = box

    return {
        "signature": {
            "present": signature_box is not None,
            "bbox": signature_box
        },
        "stamp": {
            "present": stamp_box is not None,
            "bbox": stamp_box
        }
    }
