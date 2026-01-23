# utils/confidence.py

def compute_confidence(fields):
    """
    Confidence based only on core extracted fields
    (not on signature/stamp presence)
    """
    score = 0
    total = 4  # dealer, model, hp, cost

    if fields.get("dealer_name") is not None:
        score += 1
    if fields.get("model_name") is not None:
        score += 1
    if fields.get("horse_power") is not None:
        score += 1
    if fields.get("asset_cost") is not None:
        score += 1

    return round(score / total, 2)

