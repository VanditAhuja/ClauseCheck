from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from summarizer import summarize_document
from risk_detector import detect_risk
from services.parser import extract_text_from_pdf
from clause_comparator import compare_clauses
from chunker import chunk_text
from embeddings import create_embedding
from vector_store import store_chunks
from rag import ask_question
app = FastAPI(title="ClauseCheck API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
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

    # Chunk and store for Q&A
    chunks = chunk_text(text)
    embeddings = [create_embedding(chunk) for chunk in chunks]
    store_chunks(chunks, embeddings)

    return {
        "filename": file.filename,
        "text": text,
        "summary": summary,
        "risk": risk,
        "clauses": clauses
    }
@app.post("/ask")
async def ask(question: str = Form(...)):
    answer = ask_question(question)
    return {"answer": answer}
import os
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
   