import json
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


print("\n========== ENTITY TESTS ==========\n")

print(
    "MX-01 vs MX01:",
    match_entity("MX-01", "MX01")
)

print(
    "MX-01 vs Machine 01:",
    match_entity("MX-01", "Machine 01")
)

print(
    "MX-01 vs MX-02:",
    match_entity("MX-01", "MX-02")
)


print("\n========== CLAIM TESTS ==========\n")

print(
    "temperature vs temperature:",
    same_claim("temperature", "temperature")
)

print(
    "temperature vs pressure:",
    same_claim("temperature", "pressure")
)


print("\n========== VALUE TESTS ==========\n")

print(
    compare_values(
        72,
        "°C",
        72,
        "°C"
    )
)

print(
    compare_values(
        72,
        "°C",
        91,
        "°C"
    )
)


print("\n========== MX-01 VERIFICATION ==========\n")

with open(
    "sample_data/mx01_sample.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

result = verify_claims(data["claims"])

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)