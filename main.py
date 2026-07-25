from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.summarizer import summarize_document
from backend.risk_detector import detect_risk
from backend.services.parser import extract_text_from_pdf

app = FastAPI(title="ClauseCheck API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def health_check():
    return {
        "status": "ClauseCheck API is running"
    }



@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):

    # Read uploaded PDF
    file_bytes = await file.read()

    # Extract text from PDF
    text = extract_text_from_pdf(file_bytes)


    summary = summarize_document(text)


    risk = detect_risk(text)

    # Return response
    return {
        "filename": file.filename,
        "text": text,
        "summary": summary,
        "risk": risk
    }