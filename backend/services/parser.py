import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_chunks = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_chunks.append(page.get_text())
    return "\n".join(text_chunks).strip()