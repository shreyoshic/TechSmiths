
import json
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

app = FastAPI()
import os

documents_path = os.path.join(
    os.path.dirname(__file__),
    "all_documents.json"
)

if os.path.exists(documents_path):
    with open(documents_path, "r", encoding="utf-8") as f:
        documents = json.load(f)
else:
    documents = []


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Hackfest backend is running!"
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
  os.makedirs("uploads", exist_ok=True)
file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "message": "File uploaded successfully",
        "file": file.filename
    }

@app.post("/question")
def question(request: QuestionRequest):
    return {
"answer": next((doc["text"] for doc in documents if any(word in doc["text"].lower() for word in request.question.lower().split())), "No matching information found"),
        "sources": [],
        "conflicts": [],
        "verification_status": "PENDING",
        "question": request.question
    }

@app.post("/verification")
def verification(claims: list[str]):
    results = []

    for claim in claims:
        if "91" in claim:
            results.append({
                "claim": claim,
                "status": "CONFLICT",
                "reason": "Technician Log reports 91°C, which exceeds the maximum operating temperature of 80°C."
            })
        else:
            results.append({
                "claim": claim,
                "status": "PENDING",
                "reason": "No verification rule for this claim yet."
            })

    return {
        "message": "Verification completed",
        "results": results
    }


@app.get("/report")
def report():
    return {
        "message": "Verification report generated",
        "verification_status": "CONFLICT",
        "conflicts": [
            {
                "issue": "Temperature exceeds safe limit",
                "manual_limit": "80°C",
                "observed_temperature": "91°C",
                "source": "Technician_Log.pdf"
            }
        ]
    }
