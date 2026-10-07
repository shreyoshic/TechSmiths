import re

ENTITY_ALIASES = {
    "mx01": {
        "mx01",
        "mx-01",
        "machine01",
        "machine 01",
        "machine-01"
    }
}


def normalize_entity(entity: str) -> str:
    entity = entity.lower().strip()
    entity = re.sub(r"[\s_-]+", "", entity)
    return entity


def match_entity(entity1: str, entity2: str) -> bool:
    e1 = normalize_entity(entity1)
    e2 = normalize_entity(entity2)

    if e1 == e2:
        return True

    for canonical, aliases in ENTITY_ALIASES.items():
        normalized_aliases = {
            normalize_entity(alias)
            for alias in aliases
        }

        if e1 in normalized_aliases and e2 in normalized_aliases:
            return True

    return False