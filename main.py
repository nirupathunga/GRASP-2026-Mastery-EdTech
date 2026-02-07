from fastapi import FastAPI, UploadFile, File, HTTPException
import pymupdf4llm
import os
import shutil
from engine_brain import get_blooms_assessment  # Importing the brain logic you already have

app = FastAPI()

# Create a temporary folder for uploads
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-syllabus")
async def upload_syllabus(file: UploadFile = File(...)):
    # 1. Basic Validation
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported!")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # 2. Save the file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Extract Content using PyMuPDF4LLM (Markdown is best for LLMs!)
        # This converts the PDF to clean Markdown text
        md_text = pymupdf4llm.to_markdown(file_path)

        # 4. Send to Brain (GPT-4o) for Bloom's Mapping
        # We pass the extracted markdown text to our brain engine
        analysis_result = get_blooms_assessment(md_text)

        # 5. Clean up the temp file
        os.remove(file_path)

        return {
            "filename": file.filename,
            "status": "Success",
            "analysis": analysis_result
        }

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")