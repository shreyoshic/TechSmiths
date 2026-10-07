"""Evidence validation independent of embedding/model dependencies."""
import json
from pathlib import Path


def load_evidence(path: Path):
    records = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(records, list):
        raise ValueError('Evidence must be a JSON array')
    accepted = []
    for position, item in enumerate(records):
        if not isinstance(item, dict):
            raise ValueError(f'Record {position} must be an object')
        metadata = item.get('metadata', {})
        if not isinstance(metadata, dict):
            raise ValueError(f'Record {position}: metadata must be an object')
        if metadata.get('verified') is not True or metadata.get('status') == 'placeholder':
            continue
        for key in ('evidence_id', 'text', 'source_reference', 'location'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'Verified record {position}: {key} is required')
        if item['location'].strip().lower() == 'unknown':
            raise ValueError(f'Verified record {position}: precise source location is required')
        if 'REPLACE WITH' in item['text'].upper():
            raise ValueError(f'Verified record {position}: placeholder text is forbidden')
        accepted.append(item)
    return accepted
