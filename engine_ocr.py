import pytesseract
from PIL import Image
import pymupdf4llm
import os

def extract_text_from_image(image_path):
    """Handles standalone images (PNG/JPG) using Tesseract."""
    # Open the image using Pillow
    img = Image.open(image_path)
    # Extract text using pytesseract
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf_ocr(pdf_path):
    """Handles scanned PDFs by converting pages to images first."""
    # PyMuPDF4LLM is great for digital PDFs, but for scans, 
    # Tesseract is better as a fallback.
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text