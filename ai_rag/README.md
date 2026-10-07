# TechSmiths — Embeddings + FAISS MX-01 Evidence Retrieval

This standalone add-on embeds verified evidence with Sentence Transformers,
searches a FAISS cosine-similarity index, and returns original source references
and source locations beside each retrieved excerpt. The frontend is served by
the same FastAPI service and can also be embedded into an existing frontend by
importing `frontend/ai-rag.js` and calling its two exported functions.

## Run

Use Python 3.10 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Open http://localhost:8000. The first nonempty index build downloads
`sentence-transformers/all-MiniLM-L6-v2`; later runs can use the local cache.
Set `EMBEDDING_MODEL` to a compatible local model directory to run offline.
Set `EVIDENCE_FILE` to another JSON corpus path if needed. Restart after updates.

## Supply actual MX-01 evidence

**No verified MX-01 source material was available in the supplied attachments.**
All three attachments are identical saved GitHub repository overview pages,
not the application source or evidence files. The older package contained only
a placeholder. The shipped corpus is therefore empty; the service returns no
evidence until real source chunks are supplied. No sample text is presented as
actual evidence, and no actual-source retrieval has been verified.

Each chunk must have this shape (the following is a schema illustration only):

```json
{
  "evidence_id": "MX-01",
  "text": "Exact excerpt from your source document",
  "source_reference": "your-document.pdf#page=2",
  "source_type": "document",
  "location": "page 2, paragraph 3",
  "metadata": {"verified": true}
}
```

Put the chunks in a JSON array in `data/mx01_evidence.json`. Preserve source
identifiers and precise page/section/line locations from the ingestion pipeline.
`verified: true` is an ingestion assertion, not independent source verification
by this service. Unverified/placeholder records are excluded; malformed verified
records fail startup. Use short passages with one source location per chunk.

## API

```bash
curl http://localhost:8000/api/mx-01/evidence \
  -H 'Content-Type: application/json' \
  -d '{"query":"What evidence supports MX-01?","top_k":5,"min_score":0.35}'
```

The response contains `evidence` (text, source_reference, location, metadata,
cosine similarity score) and deduplicated `source_references`. Empty results
have status `no_relevant_verified_evidence`. `/api/retrieve` also supports an
optional `evidence_id` filter. Filtering occurs before selecting top-k.
Scores are similarity values, not confidence probabilities. Calibrate the
configurable threshold against real queries; 0.35 is a starting value.

This service returns source excerpts, not generated answers. FAISS indexes are
built in memory at startup. For cross-origin embedding set `CORS_ORIGINS` to a
comma-separated list of trusted frontend origins; localhost:5500 is the default.
Keep the service local or place it behind your existing authentication before
exposing confidential evidence.

## Validation

```bash
pip install httpx
python -m unittest discover -s tests -v
```

Tests use actual FAISS with deterministic test embeddings (no model download),
and cover pre-filtering, source metadata, thresholds, empty evidence, malformed
records, and request validation. They do not validate semantic relevance of the
production model against actual MX-01 evidence.
