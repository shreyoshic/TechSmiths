
import re

# Add equipment aliases here as needed.
ENTITY_ALIASES = {
    "mx01": [
        "MX-01",
        "MX01",
        "Machine 01",
        "Machine-01",
    ],
    "mx02": [
        "MX-02",
        "MX02",
        "Machine 02",
        "Machine-02",
    ],
}


def normalize_entity(entity: str) -> str:
    """Normalize spacing, hyphens, underscores, and case."""
    if not isinstance(entity, str):
        return ""

    return re.sub(r"[\s_-]+", "", entity.strip().lower())


def match_entity(entity1: str, entity2: str) -> bool:
    """Return True when two names refer to the same known entity."""
    e1 = normalize_entity(entity1)
    e2 = normalize_entity(entity2)

    if not e1 or not e2:
        return False

    if e1 == e2:
        return True

    for canonical, aliases in ENTITY_ALIASES.items():
        known_names = {
            normalize_entity(canonical),
            *(normalize_entity(alias) for alias in aliases),
        }

        if e1 in known_names and e2 in known_names:
            return True

    return False
