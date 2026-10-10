# Person 6 - Integration Checklist

## Project
Multi Source Ingestion into a Single Verifiable Document

## Purpose
Verify that the project modules work together to produce a verifiable document with reliable source references.

## Integration Checklist

| No. | Integration Check | Expected Result | Status |
|---|---|---|---|
| 1 | Frontend sends uploaded documents to backend | Backend receives the documents successfully | NOT TESTED |
| 2 | Backend sends PDFs to document extraction | Text is extracted from PDF documents | PARTIALLY TESTED |
| 3 | Backend sends scanned images to OCR | Text is extracted from image documents | PASS - Standalone Test |
| 4 | Extracted text is passed to AI/RAG | Evidence is prepared for retrieval | BLOCKED - Real evidence unavailable |
| 5 | Retrieval returns relevant evidence | Relevant excerpts and source references are returned | PASS - Unit Tests Only |
| 6 | Entity matcher identifies equivalent machine names | Equivalent entity names are matched | PASS - Module Test |
| 7 | Claim comparator compares matching claims | Equivalent claims are identified | PASS - Module Test |
| 8 | Conflict detector identifies conflicting values | Conflicting values are reported | PASS - Module Test |
| 9 | Verifier preserves source references | Source document, page, and source hash are included | PASS - Module Test |
| 10 | Verification result is returned to backend | Backend receives the verification result | NOT TESTED |
| 11 | Frontend displays final verified output | User can see results and source references | NOT TESTED |
| 12 | Complete workflow runs using MX-01 documents | Upload through final output works successfully | NOT TESTED |

## Known Integration Blockers

1. The AI/RAG evidence file currently contains no evidence records.
2. Real MX-01 evidence retrieval cannot be validated until verified evidence is supplied.
3. The complete frontend-to-backend workflow has not yet been tested.
4. The relationship between extraction output, retrieval input, verification input, and final output must be confirmed.

## Integration Procedure

1. Confirm that each module runs independently.
2. Confirm that the backend can access document extraction and OCR outputs.
3. Confirm that extracted evidence is converted into the format required by AI/RAG.
4. Confirm that retrieval returns evidence with source references.
5. Confirm that verification receives the correct entity, claim, value, unit, and source metadata.
6. Confirm that the final verification result reaches the frontend.
7. Test the complete workflow with actual MX-01 documents.
8. Record failures, missing connections, and fixes.
9. Repeat failed tests after corrections.

## Completion Criteria

- All modules communicate using compatible data formats.
- Source references are preserved throughout the workflow.
- Conflicts are identified correctly.
- Real MX-01 evidence is available for retrieval testing.
- The end-to-end workflow completes successfully.


