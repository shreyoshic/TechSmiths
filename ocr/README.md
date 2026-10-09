# Multi-Source Document Extraction

A document-processing module for the hackathon problem
"Multi Source Ingestion into a Single Verifiable Document".

It extracts text from multiple file formats and converts it into a
common JSON structure for downstream processing and verification.

## Supported File Types

- PDF
- TXT and LOG
- DOCX
- PPTX
- XLSX
- CSV
- JPG, JPEG and PNG

## Features

- PDF text extraction using PyMuPDF
- OCR for scanned PDFs and images using Tesseract
- Extraction from Word, PowerPoint, Excel and CSV files
- SHA-256 source hash for each file
- Source references for pages, slides and sheets
- Common JSON output
- Extraction method recorded as text or OCR
- OCR confidence estimate
- Per-file error handling

## Output

Extracted records are saved to `output/all_documents.json`.

Each record contains `document`, `page`, `text`, `source_hash`,
`extraction_method` and `ocr_confidence`.

## Setup

Install Python dependencies:

`pip install -r requirements.txt`

Tesseract OCR must be installed separately for OCR functionality.

## Usage

1. Place supported files inside `documents/`.
2. Run `python3 extract_text.py`.
3. Find the results in `output/all_documents.json`.
