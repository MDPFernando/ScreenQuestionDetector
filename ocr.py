import pytesseract
from PIL import Image
import os

# Common default installation path for Tesseract on Windows
tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

def extract_text(image_path="test.png"):
    try:
        # Open the image captured in Phase 1
        img = Image.open(image_path)
        
        # Run Tesseract OCR on the image
        text = pytesseract.image_to_string(img)
        
        print("--- Extracted Text ---")
        print(text.strip())
        print("----------------------")
        
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not in your PATH. Please ensure Tesseract-OCR is installed.")
        return ""
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""

if __name__ == "__main__":
    extract_text()
