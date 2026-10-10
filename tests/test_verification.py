
import json
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from verification.entity_matcher import match_entity
from verification.claim_comparator import (
    same_claim,
    compare_values,
)
from verification.conflict_detector import (
    detect_conflict,
)
from verification.verifier import verify_claims


# Original tests

def test_entity_alias_mx01():
    assert match_entity("MX-01", "MX01") is True


def test_entity_alias_machine01():
    assert match_entity("MX-01", "Machine 01") is True


def test_different_entities():
    assert match_entity("MX-01", "MX-02") is False


def test_same_claim():
    assert same_claim("temperature", "temperature") is True


def test_different_claims():
    assert same_claim("temperature", "pressure") is False


def test_identical_values():
    result = compare_values(72, "°C", 72, "°C")
    assert result["status"] == "MATCH"


def test_conflicting_values():
    result = compare_values(72, "°C", 91, "°C")
    assert result["status"] == "CONFLICT"


def test_sample_claims():
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    sample_path = os.path.join(
        project_root, "sample_data", "mx01_sample.json"
    )

    with open(sample_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    result = verify_claims(data["claims"])

    assert isinstance(result, dict)
    assert "verification_status" in result
    assert "matches" in result
    assert "conflicts" in result


# New edge-case tests

def test_incompatible_units():
    result = compare_values(1, "bar", 100, "kPa")
    assert result["status"] == "INCOMPARABLE"


def test_missing_value():
    claim1 = {
        "entity": "MX-01",
        "claim": "temperature",
        "value": 72,
        "unit": "C",
    }
    claim2 = {
        "entity": "MX01",
        "claim": "temperature",
        "unit": "C",
    }

    result = detect_conflict(claim1, claim2)
    assert result["status"] == "UNCERTAIN"


def test_different_entities_are_not_compared():
    claim1 = {
        "entity": "MX-01",
        "claim": "temperature",
        "value": 72,
        "unit": "C",
    }
    claim2 = {
        "entity": "MX-02",
        "claim": "temperature",
        "value": 91,
        "unit": "C",
    }

    result = detect_conflict(claim1, claim2)
    assert result["status"] == "NO_CONFLICT"


def test_different_claims_are_not_compared():
    claim1 = {
        "entity": "MX-01",
        "claim": "temperature",
        "value": 72,
        "unit": "C",
    }
    claim2 = {
        "entity": "MX-01",
        "claim": "pressure",
        "value": 91,
        "unit": "C",
    }

    result = detect_conflict(claim1, claim2)
    assert result["status"] == "NO_CONFLICT"


def test_missing_source_metadata_does_not_crash():
    claims = [
        {
            "entity": "MX-01",
            "claim": "temperature",
            "value": 72,
            "unit": "C",
        },
        {
            "entity": "MX01",
            "claim": "temperature",
            "value": 91,
            "unit": "C",
        },
    ]

    result = verify_claims(claims)

    assert result["verification_status"] == "CONFLICTS_FOUND"
    assert result["conflict_count"] == 1
    assert (
        result["conflicts"][0]["sources"][0]["document"]
        == "Unknown source"
    )
