import os
from PIL import Image, UnidentifiedImageError
import pytesseract

def run_ocr_pipeline(file_path: str) -> str:
    print(f"[*] Starting OCR extraction for: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"[!] Error: File not found -> {file_path}")
        return ""

    try:
        image_buffer = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image_buffer)
        return extracted_text

    except UnidentifiedImageError:
        print(f"[!] Format Error: {file_path} is not a valid image.")
        return ""
    except pytesseract.TesseractError as e:
        print(f"[!] Tesseract Engine Error processing {file_path}: {e}")
        return ""
    except Exception as e:
        print(f"[!] Unexpected OCR Error: {e}")
        return ""
