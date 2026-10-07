def normalize_claim(claim: str) -> str:
    claim = claim.lower().strip()

    aliases = {
        "temp": "temperature",
        "temperature": "temperature",
        "operating temperature": "temperature"
    }

    return aliases.get(claim, claim)


def same_claim(claim1: str, claim2: str) -> bool:
    return normalize_claim(claim1) == normalize_claim(claim2)


def compare_values(value1, unit1, value2, unit2):
    unit1 = unit1 or ""
    unit2 = unit2 or ""

    if unit1.lower() != unit2.lower():
        return {
            "status": "INCOMPARABLE",
            "reason": "Different units"
        }

    if value1 == value2:
        return {
            "status": "MATCH",
            "reason": "Values are identical"
        }

    return {
        "status": "CONFLICT",
        "reason": f"Different values: {value1}{unit1} vs {value2}{unit2}"
    }