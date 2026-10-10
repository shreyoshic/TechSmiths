
from .entity_matcher import match_entity
from .claim_comparator import same_claim, compare_values


def detect_conflict(claim1: dict, claim2: dict) -> dict:
    entity1 = claim1.get("entity", "")
    entity2 = claim2.get("entity", "")

    if not match_entity(entity1, entity2):
        return {
            "status": "NO_CONFLICT",
            "reason": "Different entities",
        }

    property1 = claim1.get("claim", "")
    property2 = claim2.get("claim", "")

    if not same_claim(property1, property2):
        return {
            "status": "NO_CONFLICT",
            "reason": "Different claims",
        }

    if "value" not in claim1 or "value" not in claim2:
        return {
            "status": "UNCERTAIN",
            "reason": "One or both claims are missing a value",
        }

    return compare_values(
        claim1["value"],
        claim1.get("unit", ""),
        claim2["value"],
        claim2.get("unit", ""),
    )
