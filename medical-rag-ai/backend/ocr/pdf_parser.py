import pypdf
import io
from pdf2image import convert_from_bytes
from PIL import Image
from typing import Optional, List

def parse_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file.
    First tries to extract text directly (for digital PDFs).
    If that fails or returns minimal text, returns empty string to trigger OCR fallback.
    """
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def convert_pdf_to_images(file_bytes: bytes, dpi: int = 200) -> List[Image.Image]:
    """
    Convert PDF pages to PIL Images for OCR processing.
    
    Args:
        file_bytes: PDF file content as bytes
        dpi: Resolution for conversion (higher = better quality but slower)
    
    Returns:
        List of PIL Image objects, one per page
    """
    try:
        # Convert PDF to images
        images = convert_from_bytes(file_bytes, dpi=dpi)
        print(f"Converted PDF to {len(images)} image(s)")
        return images
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []

