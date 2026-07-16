from fastapi import FastAPI

app = FastAPI(title="FinePrint API")

@app.get("/")
def health_check():
    return {"status": "FinePrint API is running"}