from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.ocr.pdf_parser import parse_pdf, convert_pdf_to_images
from backend.ocr.ocr_engine import OCREngine
from PIL import Image
import io

router = APIRouter()
# Lazy Loading Wrapper
_ocr_engine_instance = None

def get_ocr_engine():
    global _ocr_engine_instance
    if _ocr_engine_instance is None:
        try:
             _ocr_engine_instance = OCREngine()
        except Exception as e:
             print(f"Warning: OCR Engine failed to load: {e}")
             return None
    return _ocr_engine_instance

@router.post("/upload-report", summary="Upload PDF or Image and extract text")
async def upload_report(file: UploadFile = File(...)):
    if file.content_type == "application/pdf":
        content = await file.read()
        
        # First, try to extract text directly (for digital PDFs)
        text = parse_pdf(content)
        
        # If we got substantial text, use it
        if text.strip() and len(text.strip()) > 50:
            print(f"DEBUG: Extracted {len(text)} characters from digital PDF")
            return {"text": text, "extracted": True, "method": "digital_pdf"}
        
        # Otherwise, treat as scanned PDF and use Gemini OCR
        print("DEBUG: Digital PDF extraction failed or minimal text. Using Gemini OCR...")
        engine = get_ocr_engine()
        if not engine:
            raise HTTPException(status_code=500, detail="OCR Engine not available for scanned PDF.")
        
        # Convert PDF pages to images
        images = convert_pdf_to_images(content)
        if not images:
            return {"text": "", "note": "Failed to convert PDF to images for OCR.", "extracted": False}
        
        # Process each page with Gemini OCR
        all_text = []
        for idx, image in enumerate(images):
            print(f"DEBUG: Processing page {idx + 1}/{len(images)} with Gemini OCR...")
            page_text = engine.process_image(image)
            all_text.append(f"--- Page {idx + 1} ---\n{page_text}")
        
        combined_text = "\n\n".join(all_text)
        print(f"DEBUG: Extracted {len(combined_text)} characters from scanned PDF using OCR")
        return {"text": combined_text, "extracted": True, "method": "gemini_ocr_pdf"}
    
    elif file.content_type.startswith("image/"):
        engine = get_ocr_engine()
        if not engine:
             raise HTTPException(status_code=500, detail="OCR Engine not available/failed to load.")
        
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")
        text = engine.process_image(image)
        print(f"DEBUG: Extracted OCR Text: {text[:500]}...") # Log first 500 chars
        return {"text": text, "extracted": True, "method": "gemini_ocr_image"}
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

