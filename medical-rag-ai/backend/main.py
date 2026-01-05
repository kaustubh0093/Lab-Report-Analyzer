from fastapi import FastAPI
from backend.config import settings
from backend.api import upload, analyze, stream, chat

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="AI Medical Report Analyzer (Clinical RAG)"
)

app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(stream.router, prefix="/api", tags=["System"])

@app.get("/")
def root():
    return {"message": "Welcome to Medical RAG AI API. Visit /docs for swagger."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
