
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
import re

from ocr.extract_text import extract_file, SUPPORTED_EXTENSIONS

app = FastAPI(title="Hackfest Backend")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "ocr" / "output"
INDEX_FILE = OUTPUT_DIR / "all_documents.json"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


def load_index():
    if not INDEX_FILE.exists():
        return []

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_index(records):
    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)


def index_file(file_path):
    # Extract first so a failed extraction does not erase
    # any previously indexed records for this document.
    new_records = extract_file(str(file_path))

    records = load_index()
    records = [
        record for record in records
        if record.get("document") != file_path.name
    ]
    records.extend(new_records)
    save_index(records)

    return new_records


def index_existing_uploads():
    for file_path in sorted(UPLOAD_DIR.iterdir()):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            index_file(file_path)
            print(f"Indexed: {file_path.name}")
        except Exception as error:
            print(f"Could not index {file_path.name}: {error}")


def extract_temperature_records(records):
    results = []
    pattern = r"(-?\d+(?:\.\d+)?)\s*°\s*C\b"

    for record in records:
        text = record.get("text", "")

        for match in re.finditer(pattern, text, re.IGNORECASE):
            results.append({
                "temperature_celsius": float(match.group(1)),
                "document": record.get("document"),
                "page": record.get("page")
            })

    return results


def get_verification_status(temperature_records):
    values = {
        item["temperature_celsius"]
        for item in temperature_records
    }

    return "REVIEW_REQUIRED" if len(values) > 1 else "PENDING"


@app.on_event("startup")
def startup():
    index_existing_uploads()


@app.get("/")
def home():
    return {"message": "Hackfest Backend is running!"}


# 1. Upload and extract documents
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = Path(file.filename or "uploaded_file").name

    if not filename or filename == ".":
        raise HTTPException(status_code=400, detail="Invalid filename")

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    file_path = UPLOAD_DIR / filename
    content = await file.read()

    try:
        with open(file_path, "wb") as saved_file:
            saved_file.write(content)
    finally:
        await file.close()

    try:
        records = index_file(file_path)

        return {
            "message": "File uploaded and extracted successfully",
            "file": filename,
            "records_extracted": len(records),
            "extraction_status": "SUCCESS"
        }

    except Exception as error:
        return {
            "message": "File uploaded, but text extraction failed",
            "file": filename,
            "extraction_status": "FAILED",
            "reason": str(error)
        }


# 2. Search extracted document text
@app.post("/question")
def question(request: QuestionRequest):
    records = load_index()
    question_text = request.question.lower()

    stop_words = {
        "what", "is", "the", "a", "an", "of", "in", "to",
        "for", "and", "does", "do", "tell", "me", "about",
        "please", "can", "you", "was", "were", "recorded",
        "found", "show", "give", "find", "with", "on", "at",
        "it", "this", "that"
    }

    question_words = (
        set(re.findall(r"[a-z0-9]+", question_text)) - stop_words
    )

    matches = []

    for record in records:
        text = record.get("text", "")
        text_lower = text.lower()

        score = sum(
            1 for word in question_words
            if len(word) > 1 and word in text_lower
        )

        if score > 0:
            matches.append((score, record))

    matches.sort(key=lambda item: item[0], reverse=True)

    temperature_words = {
        "temperature", "temperatures", "temp",
        "celsius", "degree", "degrees"
    }

    asks_temperature = bool(
        set(re.findall(r"[a-z]+", question_text))
        & temperature_words
    )

    temperature_records = (
        extract_temperature_records(records)
        if asks_temperature else []
    )

    if matches:
        best = matches[0][1]
        answer = best.get("text", "")[:1000]
        sources = [
            f'{best.get("document")}, page {best.get("page")}'
        ]
    else:
        answer = "No matching information found in extracted documents."
        sources = []

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources,
        "conflicts": temperature_records,
        "verification_status": get_verification_status(
            temperature_records
        )
    }


# 3. Verification endpoint
@app.get("/verification")
def verification():
    records = load_index()
    temperatures = extract_temperature_records(records)

    unique_values = sorted({
        item["temperature_celsius"] for item in temperatures
    })

    status = get_verification_status(temperatures)

    if status == "REVIEW_REQUIRED":
        message = (
            "Different temperature values were found. "
            "Review their context before deciding whether they conflict."
        )
    elif temperatures:
        message = (
            "Temperature values were found, but a conflict "
            "has not been confirmed."
        )
    else:
        message = "No readable Celsius temperature values were detected."

    return {
        "status": status,
        "message": message,
        "temperature_values_found": len(temperatures),
        "unique_temperature_values": unique_values,
        "findings": temperatures
    }


# 4. JSON report endpoint
@app.get("/report")
def report():
    records = load_index()
    temperatures = extract_temperature_records(records)

    documents = {}

    for record in records:
        filename = record.get("document", "unknown")

        if filename not in documents:
            documents[filename] = set()

        documents[filename].add(str(record.get("page", "")))

    status = get_verification_status(temperatures)

    return {
        "report_status": status,
        "documents_count": len(documents),
        "documents": [
            {
                "filename": filename,
                "pages": len(page_numbers)
            }
            for filename, page_numbers in documents.items()
        ],
        "temperatures_found": temperatures,
        "message": (
            "Different temperature values detected; review their context."
            if status == "REVIEW_REQUIRED"
            else "No differing temperature values detected, "
                 "or more information is needed."
        )
    }
