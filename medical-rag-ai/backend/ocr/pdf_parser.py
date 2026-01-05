import pypdf
import io

def parse_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file.
    Does NOT handle scanned PDFs via OCR in this simple function (that would require converting pages to images).
    For scanned PDFs, the client should convert to images or we use headers.
    
    For MVP, we extract text if digital, else return empty string (triggering OCR fallback in logic).
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
