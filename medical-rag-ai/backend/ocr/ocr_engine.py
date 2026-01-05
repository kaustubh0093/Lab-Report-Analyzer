import google.generativeai as genai
from PIL import Image
import io
from backend.config import settings

class OCREngine:
    def __init__(self):
        print("Initializing Gemini Vision for OCR...")
        if not settings.GOOGLE_API_KEY:
             print("ERROR: GOOGLE_API_KEY missing for OCR.")
             return
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.LLM_MODEL)
        print("Gemini Vision OCR Ready.")

    def process_image(self, image: Image.Image) -> str:
        """
        Uses Gemini Vision to extract text from an image (screenshot/photo).
        """
        prompt = "Extract all text from this medical lab report image exactly as it appears. Maintain the structure as much as possible."
        
        try:
            response = self.model.generate_content([prompt, image])
            text = response.text
            print(f"DEBUG: Gemini OCR Extracted {len(text)} characters.")
            return text
        except Exception as e:
            print(f"ERROR: Gemini OCR failed: {e}")
            return "Error extracting text from image."
