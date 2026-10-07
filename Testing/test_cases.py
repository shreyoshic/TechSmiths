import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from verification.entity_matcher import match_entity
from verification.claim_comparator import (
    same_claim,
    compare_values
)
from verification.verifier import verify_claims


# =====================================================
# 1. ENTITY RESOLUTION TESTS
# =====================================================

assert match_entity("MX-01", "MX01") is True

assert match_entity(
    "MX-01",
    "Machine 01"
) is True

assert match_entity(
    "Machine-01",
    "MX01"
) is True

assert match_entity(
    "MX-01",
    "MX-02"
) is False


# =====================================================
# 2. CLAIM TESTS
# =====================================================

assert same_claim(
    "temperature",
    "temperature"
) is True

assert same_claim(
    "temp",
    "temperature"
) is True

assert same_claim(
    "operating temperature",
    "temperature"
) is True

assert same_claim(
    "temperature",
    "pressure"
) is False


# =====================================================
# 3. VALUE TESTS
# =====================================================

result = compare_values(
    72,
    "°C",
    72,
    "°C"
)

assert result["status"] == "MATCH"


result = compare_values(
    72,
    "°C",
    91,
    "°C"
)

assert result["status"] == "CONFLICT"


result = compare_values(
    72,
    "°C",
    161.6,
    "°F"
)

assert result["status"] == "INCOMPARABLE"


# =====================================================
# 4. CONFLICT TEST
# =====================================================

claims = [
    {
        "entity": "MX-01",
        "claim": "temperature",
        "value": 72,
        "unit": "°C",
        "source": "inspection_report.pdf",
        "page": 3,
        "classification": "inspection",
        "source_hash": "hash-inspection"
    },

    {
        "entity": "Machine 01",
        "claim": "temperature",
        "value": 91,
        "unit": "°C",
        "source": "technician_log.txt",
        "page": 1,
        "classification": "technician_log",
        "source_hash": "hash-technician"
    }
]

result = verify_claims(claims)

assert result["verification_status"] == "CONFLICTS_FOUND"

assert result["conflict_count"] == 1

assert result["conflicts"][0]["values"][0]["value"] == 72

assert result["conflicts"][0]["values"][1]["value"] == 91


# =====================================================
# 5. MATCH TEST
# =====================================================

matching_claims = [
    {
        "entity": "MX-01",
        "claim": "temperature",
        "value": 72,
        "unit": "°C",
        "source": "inspection_report.pdf",
        "page": 3
    },

    {
        "entity": "MX01",
        "claim": "temperature",
        "value": 72,
        "unit": "°C",
        "source": "maintenance_report.pdf",
        "page": 2
    }
]

result = verify_claims(matching_claims)

assert result["verification_status"] == "VERIFIED"

assert len(result["matches"]) == 1

assert result["matches"][0]["value"] == 72


# =====================================================
# 6. DIFFERENT ENTITY TEST
# =====================================================

different_entities = [
    {
        "entity": "MX-01",
        "claim": "temperature",
        "value": 72,
        "unit": "°C",
        "source": "report1.pdf",
        "page": 1
    },

    {
        "entity": "MX-02",
        "claim": "temperature",
        "value": 91,
        "unit": "°C",
        "source": "report2.pdf",
        "page": 1
    }
]

result = verify_claims(different_entities)

assert result["conflict_count"] == 0


# =====================================================
# SUCCESS
# =====================================================

print()
print("========================================")
print("      ALL P5 TESTS PASSED")
print("========================================")
print()