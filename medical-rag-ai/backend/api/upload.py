from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.ocr.pdf_parser import parse_pdf
from backend.ocr.ocr_engine import OCREngine
from PIL import Image
import io

router = APIRouter()
# Instantiate the REAL engine. This will load models into memory on startup (or first call depending on import time).
# We might want to lazy load this if startup is too slow, but for now we initialize it.
# To avoid global startup cost blocking entire app if unused, we could use a singleton pattern or lru_cache,
# but for simplicity we initialize it globaly or inside the endpoint.
# Initializing globally is better for performance after first load.
# Lazy Loading Wrapper
_ocr_engine_instance = None

def get_ocr_engine():
    global _ocr_engine_instance
    if _ocr_engine_instance is None:
        try:
             # Import here to avoid top-level dependency if possible, or just init here
             _ocr_engine_instance = OCREngine()
        except Exception as e:
             print(f"Warning: OCR Engine failed to load: {e}")
             return None
    return _ocr_engine_instance

@router.post("/upload-report", summary="Upload PDF or Image and extract text")
async def upload_report(file: UploadFile = File(...)):
    if file.content_type == "application/pdf":
        content = await file.read()
        text = parse_pdf(content)
        if not text.strip():
             return {"text": "", "note": "Scanned PDF detected. Please upload image or searchable PDF.", "extracted": False}
        return {"text": text, "extracted": True}
    
    elif file.content_type.startswith("image/"):
        engine = get_ocr_engine()
        if not engine:
             raise HTTPException(status_code=500, detail="OCR Engine not available/failed to load.")
        
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")
        text = engine.process_image(image)
        print(f"DEBUG: Extracted OCR Text: {text[:500]}...") # Log first 500 chars
        return {"text": text, "extracted": True}
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
