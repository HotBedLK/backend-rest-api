from fastapi import FastAPI

app = FastAPI(title="Admin Service")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "user"}
