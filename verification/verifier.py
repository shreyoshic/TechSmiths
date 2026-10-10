
from .conflict_detector import detect_conflict


def get_source_details(claim):
    """Keep evidence details even when some metadata is missing."""
    return {
        "document": claim.get("source", "Unknown source"),
        "page": claim.get("page"),
        "classification": claim.get("classification"),
        "source_hash": claim.get("source_hash"),
    }


def verify_claims(claims: list) -> dict:
    conflicts = []
    matches = []
    uncertain = []

    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            claim1 = claims[i]
            claim2 = claims[j]

            result = detect_conflict(claim1, claim2)
            status = result["status"]

            if status == "CONFLICT":
                conflicts.append({
                    "entity": claim1.get("entity"),
                    "matched_entities": [
                        claim1.get("entity"),
                        claim2.get("entity"),
                    ],
                    "claim": claim1.get("claim"),
                    "values": [
                        {
                            "value": claim1.get("value"),
                            "unit": claim1.get("unit", ""),
                        },
                        {
                            "value": claim2.get("value"),
                            "unit": claim2.get("unit", ""),
                        },
                    ],
                    "sources": [
                        get_source_details(claim1),
                        get_source_details(claim2),
                    ],
                    "status": "CONFLICT",
                    "reason": result.get("reason", "Values differ"),
                })

            elif status == "MATCH":
                matches.append({
                    "entity": claim1.get("entity"),
                    "claim": claim1.get("claim"),
                    "value": claim1.get("value"),
                    "unit": claim1.get("unit", ""),
                    "sources": [
                        get_source_details(claim1),
                        get_source_details(claim2),
                    ],
                    "status": "MATCH",
                })

            elif status in ("UNCERTAIN", "INCOMPARABLE"):
                uncertain.append({
                    "entities": [
                        claim1.get("entity"),
                        claim2.get("entity"),
                    ],
                    "claims": [
                        claim1.get("claim"),
                        claim2.get("claim"),
                    ],
                    "sources": [
                        get_source_details(claim1),
                        get_source_details(claim2),
                    ],
                    "status": status,
                    "reason": result.get("reason", "Could not verify"),
                })

    if conflicts:
        overall_status = "CONFLICTS_FOUND"
    elif uncertain:
        overall_status = "REVIEW_REQUIRED"
    else:
        overall_status = "VERIFIED"

    return {
        "verification_status": overall_status,
        "total_claims": len(claims),
        "matches": matches,
        "conflicts": conflicts,
        "uncertain": uncertain,
        "conflict_count": len(conflicts),
    }
