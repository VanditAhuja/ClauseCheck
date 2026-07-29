from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.summarizer import summarize_document
from backend.risk_detector import detect_risk
from backend.services.parser import extract_text_from_pdf
from backend.clause_comparator import compare_clauses
from backend.chunker import chunk_text
from backend.embeddings import create_embedding
from backend.vector_store import store_chunks
from backend.rag import ask_questionp
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
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    summary = summarize_document(text)
    risk = detect_risk(text)
    clauses = compare_clauses(text)

    return {
        "filename": file.filename,
        "text": text,
        "summary": summary,
        "risk": risk,
        "clauses": clauses
    }