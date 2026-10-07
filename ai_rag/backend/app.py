from contextlib import asynccontextmanager
from pathlib import Path
import os

import faiss
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from sentence_transformers import SentenceTransformer
from .evidence import load_evidence

ROOT = Path(__file__).resolve().parent.parent
MODEL_NAME = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
DATA_FILE = Path(os.getenv('EVIDENCE_FILE', str(ROOT / 'data/mx01_evidence.json')))


@asynccontextmanager
async def lifespan(app):
    records = load_evidence(DATA_FILE)
    app.state.records = records
    app.state.model = None
    app.state.indexes = {}
    if records:
        model = SentenceTransformer(MODEL_NAME)
        vectors = np.ascontiguousarray(model.encode(
            [r['text'] for r in records], normalize_embeddings=True,
            convert_to_numpy=True), dtype=np.float32)
        if not np.isfinite(vectors).all():
            raise ValueError('Embedding model returned non-finite vectors')
        # Each evidence group has its own index: filter BEFORE selecting top-k.
        for evidence_id in {r['evidence_id'] for r in records} | {None}:
            positions = [i for i, r in enumerate(records)
                         if evidence_id is None or r['evidence_id'] == evidence_id]
            index = faiss.IndexFlatIP(vectors.shape[1])
            index.add(vectors[positions])
            app.state.indexes[evidence_id] = (index, positions)
        app.state.model = model
    yield


app = FastAPI(title='TechSmiths MX-01 Evidence Retrieval', version='1.1.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware,
    allow_origins=[s.strip() for s in os.getenv('CORS_ORIGINS', 'http://localhost:5500').split(',')],
    allow_credentials=False, allow_methods=['GET', 'POST'], allow_headers=['Content-Type'])


class Query(BaseModel):
    query: str = Field(min_length=1, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=50)
    evidence_id: str | None = Field(default=None, min_length=1, max_length=100)
    min_score: float = Field(default=0.35, ge=-1, le=1)

    @field_validator('query')
    @classmethod
    def nonblank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('query must not be blank')
        return value


def retrieve(body, evidence_id=None):
    selected = app.state.indexes.get(evidence_id)
    if selected is None:
        return []
    index, positions = selected
    q = np.ascontiguousarray(app.state.model.encode([body.query],
        normalize_embeddings=True, convert_to_numpy=True), dtype=np.float32)
    scores, ids = index.search(q, min(body.top_k, len(positions)))
    hits = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0 or not np.isfinite(score) or float(score) < body.min_score:
            continue
        item = app.state.records[positions[int(idx)]]
        hits.append({**item, 'score': round(float(score), 4)})
    return hits


@app.get('/health')
def health():
    return {'ok': True, 'verified_chunks': len(app.state.records),
            'model': MODEL_NAME, 'status': 'ready' if app.state.records else 'no_verified_evidence'}


@app.post('/api/retrieve')
def retrieve_api(body: Query):
    return {'query': body.query, 'results': retrieve(body, body.evidence_id)}


@app.post('/api/mx-01/evidence')
def mx01_evidence(body: Query):
    hits = retrieve(body, 'MX-01')
    return {'evidence_id': 'MX-01', 'query': body.query, 'evidence': hits,
            'status': 'retrieved' if hits else 'no_relevant_verified_evidence',
            'source_references': list(dict.fromkeys(h['source_reference'] for h in hits))}


app.mount('/', StaticFiles(directory=ROOT / 'frontend', html=True), name='frontend')
