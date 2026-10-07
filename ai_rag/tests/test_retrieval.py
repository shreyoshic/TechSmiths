"""Actual FAISS search with deterministic test vectors; no model download needed."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient
from backend.app import app
from backend.evidence import load_evidence


class TestEncoder:
    def encode(self, texts, **kwargs):
        return np.array([[1., 0.] if 'motor' in t else [0., 1.] for t in texts], dtype='float32')


def record(eid, text, ref):
    return dict(evidence_id=eid, text=text, source_reference=ref,
                location='page 2, paragraph 3', metadata={'verified': True})


class RetrievalTests(unittest.TestCase):
    def test_filtered_search_and_references(self):
        records = [record('OTHER', 'motor', 'other.pdf#p2'),
                   record('MX-01', 'motor evidence', 'manual.pdf#p2'),
                   record('MX-01', 'unrelated', 'manual.pdf#p3')]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'evidence.json'
            path.write_text(json.dumps(records))
            with patch('backend.app.DATA_FILE', path), patch('backend.app.SentenceTransformer', return_value=TestEncoder()):
                with TestClient(app) as client:
                    response = client.post('/api/mx-01/evidence', json={'query': 'motor', 'top_k': 1})
                    self.assertEqual(response.status_code, 200)
                    result = response.json()
                    self.assertEqual(result['source_references'], ['manual.pdf#p2'])
                    self.assertEqual(result['evidence'][0]['location'], 'page 2, paragraph 3')
                    result = client.post('/api/mx-01/evidence', json={'query': 'motor', 'top_k': 5}).json()
                    self.assertEqual(len(result['evidence']), 1)
                    self.assertEqual(client.post('/api/retrieve', json={'query': 'motor', 'evidence_id': 'MISSING'}).json()['results'], [])
                    for body in [{'query': ' '}, {'query': 'motor', 'top_k': 0}]:
                        self.assertEqual(client.post('/api/mx-01/evidence', json=body).status_code, 422)

    def test_empty_corpus_does_not_load_model(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'evidence.json'
            path.write_text('[]')
            with patch('backend.app.DATA_FILE', path), patch('backend.app.SentenceTransformer') as encoder:
                with TestClient(app) as client:
                    self.assertEqual(client.get('/health').json()['status'], 'no_verified_evidence')
                    self.assertEqual(client.post('/api/mx-01/evidence', json={'query': 'motor'}).json()['evidence'], [])
                    self.assertEqual(client.get('/').status_code, 200)
                encoder.assert_not_called()

    def test_unverified_and_invalid_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'evidence.json'
            path.write_text(json.dumps([{'metadata': {'verified': False}}]))
            self.assertEqual(load_evidence(path), [])
            path.write_text(json.dumps([record('MX-01', 'motor', '')]))
            with self.assertRaises(ValueError):
                load_evidence(path)


if __name__ == '__main__':
    unittest.main()
