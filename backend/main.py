from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional

from verification.verifier import verify_claims


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hackfest backend is running!"
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {
        "message": "File received",
        "filename": file.filename
    }


@app.post("/question")
def question():
    return {
        "message": "Question endpoint working"
    }


# -------------------------------
# P5 VERIFICATION
# -------------------------------

class Claim(BaseModel):
    entity: str
    claim: str
    value: float
    unit: Optional[str] = ""
    source: str
    page: Optional[int] = None
    classification: Optional[str] = None
    source_hash: Optional[str] = None


class VerificationRequest(BaseModel):
    claims: List[Claim]


@app.post("/verify")
def verify(request: VerificationRequest):
    claims = [
        claim.model_dump()
        for claim in request.claims
    ]

    result = verify_claims(claims)

    return result


# Keep the original endpoint for team compatibility
@app.post("/verification")
def verification():
    return {
        "message": "Verification endpoint working"
    }


@app.get("/report")
def report():
    return {
        "message": "Report endpoint working"
    }