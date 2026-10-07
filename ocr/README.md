# Multi-Source Document Extraction

This module extracts text from multiple document formats and converts them into a common JSON structure for downstream processing.

## Supported File Types

- PDF
- TXT
- LOG

## Features

- PDF text extraction using PyMuPDF
- OCR fallback for scanned PDFs using Tesseract
- TXT and LOG extraction
- SHA-256 source hash for every file
- Page-level tracking for source citations
- Common JSON output
- Records extraction method as `text` or `ocr`
- Supports multiple files in the `documents/` folder

## Project Structure

```text
hackathon - doc extraction/
├── documents/
├── output/
├── extract_text.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
