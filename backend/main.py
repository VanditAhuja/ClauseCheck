from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.parser import extract_text_from_pdf

app = FastAPI(title="ClauseCheck API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ClauseCheck API is running"}

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    return {"filename": file.filename, "extracted_text": text}