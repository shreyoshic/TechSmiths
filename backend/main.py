from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hackfest backend is running!"}


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
    