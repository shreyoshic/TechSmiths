from .entity_matcher import match_entity
from .claim_comparator import same_claim, compare_values


def detect_conflict(claim1: dict, claim2: dict) -> dict:

    if not match_entity(claim1["entity"], claim2["entity"]):
        return {
            "status": "NO_CONFLICT",
            "reason": "Different entities"
        }

    if not same_claim(claim1["claim"], claim2["claim"]):
        return {
            "status": "NO_CONFLICT",
            "reason": "Different claims"
        }

    result = compare_values(
        claim1["value"],
        claim1.get("unit", ""),
        claim2["value"],
        claim2.get("unit", "")
    )

    return result