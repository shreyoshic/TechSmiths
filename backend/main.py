from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
from pypdf import PdfReader

app = FastAPI(title="Hackfest Backend")

# Backend storage folders
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Request model for the question endpoint
class QuestionRequest(BaseModel):
    question: str

# Temporary document list.
# We will connect the extracted document text next.
documents = []


@app.get("/")
def home():
    return {
        "message": "Hackfest Backend is running!"
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = Path(file.filename or "uploaded_file").name
    file_path = UPLOAD_DIR / filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "message": "File uploaded successfully",
        "file": filename
    }




    
   
@app.post("/question")
def question(request: QuestionRequest):
    question_words = set(request.question.lower().split())

    stop_words = {
        "what", "is", "the", "a", "an",
        "of", "in", "to", "for", "and",
        "recommended"
    }
    question_words -= stop_words

    matches = []

    # Read every PDF saved in the uploads folder
    for pdf_file in UPLOAD_DIR.glob("*.pdf"):
        try:
            reader = PdfReader(str(pdf_file))

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                text_lower = text.lower()

                score = sum(
                    1 for word in question_words
                    if word in text_lower
                )

                if score > 0:
                    matches.append(
                        (score, pdf_file.name, page_number, text)
                    )

        except Exception as error:
            print(f"Could not read {pdf_file.name}: {error}")

    matches.sort(key=lambda item: item[0], reverse=True)

    if matches:
        best_score, filename, page_number, text = matches[0]

        return {
            "question": request.question,
            "answer": text[:1000],
            "sources": [
                f"{filename}, page {page_number}"
            ],
            "conflicts": [],
            "verification_status": "PENDING"
        }

    return {
        "question": request.question,
        "answer": "No matching information found in uploaded PDFs.",
        "sources": [],
        "conflicts": [],
        "verification_status": "PENDING"
    }


@app.get("/verification")
def verification():
    return {
        "status": "PENDING",
        "message": "Document verification is not connected yet.",
        "conflicts": []
    }


@app.get("/report")
def report():
    return {
        "status": "PENDING",
        "message": "Report generation is not connected yet.",
        "documents": []
    }
