import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Medical RAG AI")
    API_VERSION = os.getenv("API_VERSION", "v1")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    HF_AUTH_TOKEN = os.getenv("HF_AUTH_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "vectorstore/index")
    
    # Model Configs
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L12-v2"
    OCR_MODEL = "microsoft/trocr-large-printed" 
    LLM_MODEL = "gemini-2.5-flash" 
    
    # Paths
    KNOWLEDGE_BASE_DIR = "knowledge_base"

settings = Settings()
