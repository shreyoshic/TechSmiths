import pymupdf
import os
import json
import hashlib
import pytesseract
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".json"):
        os.remove(os.path.join(OUTPUT_DIR, file))

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()

def fix_encoding(text):
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

def clean_text(text):
    text = fix_encoding(text)

    return "\n".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

def extract_pdf(pdf_path):

    doc = pymupdf.open(pdf_path)

    document_name = os.path.basename(pdf_path)
    source_hash = calculate_hash(pdf_path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        # Try normal text extraction first
        text = page.get_text().strip()
        extraction_method = "text"

        
        if not text:

            pix = page.get_pixmap(dpi=200)

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text = pytesseract.image_to_string(image).strip()
            extraction_method = "ocr"

        
        text = clean_text(text)

        pages.append({
            "document": document_name,
            "page": page_number,
            "text": text,
            "source_hash": source_hash,
            "extraction_method": extraction_method
        })

    doc.close()

    return pages

def extract_text_file(file_path):

    document_name = os.path.basename(file_path)
    source_hash = calculate_hash(file_path)

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="replace"
    ) as file:
        text = file.read()

    text = clean_text(text)

    return [{
        "document": document_name,
        "page": 1,
        "text": text,
        "source_hash": source_hash,
        "extraction_method": "text"
    }]

def extract_all_documents():

    supported_files = [
        file
        for file in os.listdir(DOCUMENTS_DIR)
        if file.lower().endswith((".pdf", ".txt", ".log"))
    ]

    all_documents = []

    for filename in supported_files:

        file_path = os.path.join(
            DOCUMENTS_DIR,
            filename
        )

        try:

            if filename.lower().endswith(".pdf"):
                result = extract_pdf(file_path)

            else:
                result = extract_text_file(file_path)

            all_documents.extend(result)

            output_name = (
                os.path.splitext(filename)[0] + ".json"
            )

            output_path = os.path.join(
                OUTPUT_DIR,
                output_name
            )

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    result,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("Extracted:", filename)

        except Exception as e:

            print("Failed to extract:", filename)
            print("Error:", e)

    combined_output = os.path.join(
        OUTPUT_DIR,
        "all_documents.json"
    )

    with open(
        combined_output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_documents,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "Combined output saved to output/all_documents.json"
    )

    return all_documents

if __name__ == "__main__":
    extract_all_documents()