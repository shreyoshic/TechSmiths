from .conflict_detector import detect_conflict


def verify_claims(claims: list) -> dict:

    conflicts = []
    matches = []

    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):

            claim1 = claims[i]
            claim2 = claims[j]

            result = detect_conflict(claim1, claim2)

            if result["status"] == "CONFLICT":

                conflicts.append({
                    "entity": claim1["entity"],

                    "matched_entities": [
                        claim1["entity"],
                        claim2["entity"]
                    ],

                    "claim": claim1["claim"],

                    "values": [
                        {
                            "value": claim1["value"],
                            "unit": claim1.get("unit", "")
                        },
                        {
                            "value": claim2["value"],
                            "unit": claim2.get("unit", "")
                        }
                    ],

                    "sources": [
                        {
                            "document": claim1["source"],
                            "page": claim1.get("page"),
                            "classification": claim1.get("classification"),
                            "source_hash": claim1.get("source_hash")
                        },
                        {
                            "document": claim2["source"],
                            "page": claim2.get("page"),
                            "classification": claim2.get("classification"),
                            "source_hash": claim2.get("source_hash")
                        }
                    ],

                    "status": "CONFLICT",

                    "reason": result["reason"]
                })

            elif result["status"] == "MATCH":

                matches.append({
                    "entity": claim1["entity"],
                    "claim": claim1["claim"],
                    "value": claim1["value"],
                    "unit": claim1.get("unit", ""),

                    "sources": [
                        claim1["source"],
                        claim2["source"]
                    ],

                    "status": "MATCH"
                })

    return {
        "verification_status":
            "CONFLICTS_FOUND"
            if conflicts
            else "VERIFIED",

        "total_claims": len(claims),

        "matches": matches,

        "conflicts": conflicts,

        "conflict_count": len(conflicts)
    }