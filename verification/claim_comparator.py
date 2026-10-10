
def normalize_claim(claim: str) -> str:
    """Normalize common names for the same type of claim."""
    if not isinstance(claim, str):
        return ""

    claim = " ".join(claim.lower().strip().split())

    aliases = {
        "temp": "temperature",
        "temperature": "temperature",
        "operating temperature": "temperature",
        "operating temp": "temperature",
        "pressure": "pressure",
        "operating pressure": "pressure",
        "vibration": "vibration",
        "voltage": "voltage",
    }

    return aliases.get(claim, claim)


def same_claim(claim1: str, claim2: str) -> bool:
    """Check whether two claim names represent the same property."""
    first = normalize_claim(claim1)
    second = normalize_claim(claim2)

    return bool(first) and first == second


def compare_values(value1, unit1, value2, unit2):
    """
    Compare two values.
    Never report a conflict when units differ and conversion
    has not been implemented.
    """
    unit1 = (unit1 or "").strip().lower()
    unit2 = (unit2 or "").strip().lower()

    if unit1 != unit2:
        return {
            "status": "INCOMPARABLE",
            "reason": "Different units; conversion is required",
        }

    if value1 is None or value2 is None:
        return {
            "status": "UNCERTAIN",
            "reason": "One or both values are missing",
        }

    try:
        number1 = float(value1)
        number2 = float(value2)
    except (TypeError, ValueError):
        if value1 == value2:
            return {
                "status": "MATCH",
                "reason": "Values are identical",
            }

        return {
            "status": "UNCERTAIN",
            "reason": "Values could not be compared numerically",
        }

    if number1 == number2:
        return {
            "status": "MATCH",
            "reason": "Values are identical",
        }

    return {
        "status": "CONFLICT",
        "reason": f"Different values: {value1}{unit1} vs {value2}{unit2}",
    }
