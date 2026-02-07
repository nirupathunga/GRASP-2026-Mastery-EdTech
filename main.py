import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager

# Import your custom engines
import pymupdf4llm
from engine_brain import (
    get_blooms_assessment, 
    audit_reasoning, 
    get_adaptive_instruction
)
from engine_ocr import extract_text_from_image
from engine_voice import transcribe_file  # Ensure this matches engine_voice.py
from scheduler_logic import schedule_1_4_7_nudges
from db_manager import update_db

# 1. Lifespan for APScheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the notification scheduler
    print("🚀 Starting GRASP Notification Engine...")
    yield
    # Shutdown: Clean up resources
    print("🛑 Shutting down...")

app = FastAPI(
    title="GRASP 2026 Mastery AI",
    description="Adaptive Learning Loop with Voice Feedback and Bloom's Taxonomy",
    lifespan=lifespan
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- ROOT ENDPOINT (Fixes the 404/Not Found error) ---
@app.get("/")
async def root():
    return {
        "message": "GRASP 2026 Backend is Live!",
        "documentation": "/docs",
        "team": ["Nirupathunga", "Krishnakanth", "Kamaleshwaran"]
    }

# --- PDF SYLLABUS ENDPOINT ---
@app.post("/upload-syllabus")
async def upload_syllabus(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported!")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        md_text = pymupdf4llm.to_markdown(file_path)
        analysis_result = get_blooms_assessment(md_text)
        
        os.remove(file_path)
        return {"filename": file.filename, "status": "Success", "analysis": analysis_result}
    except Exception as e:
        if os.path.exists(file_path): os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

# --- IMAGE NOTES ENDPOINT ---
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    temp_path = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")
    content = await file.read()
    with open(temp_path, "wb") as buffer:
        buffer.write(content)
    
    raw_text = extract_text_from_image(temp_path)
    analysis = get_blooms_assessment(raw_text)
    
    os.remove(temp_path)
    return {"analysis": analysis}

# --- THE MASTERY LOOP (VOICE) ---
@app.post("/test-understanding/{topic_id}")
async def test_understanding(topic_id: str, audio_file: UploadFile = File(...)):
    # Save audio temporarily for transcription
    temp_audio = os.path.join(UPLOAD_DIR, f"voice_{audio_file.filename}")
    with open(temp_audio, "wb") as buffer:
        buffer.write(await audio_file.read())

    # 1. Transcribe (Using the name imported above)
    transcript = transcribe_file(temp_audio)
    
    # 2. GPT-4o Audits the reasoning
    audit = audit_reasoning(transcript, topic_id) 
    
    # 3. Decision Logic
    if audit.get('score', 0) >= 80:
        update_db(topic_id, status="mastered")
        # Ensure your schedule function accepts topic_id
        schedule_1_4_7_nudges(topic_id) 
        response = {
            "status": "Mastered!", 
            "score": audit['score'],
            "next_topic": "Topic B", 
            "feedback": audit['feedback']
        }
    else:
        new_explanation = get_adaptive_instruction(topic_id, previous_feedback=audit['feedback'])
        response = {
            "status": "Try Again", 
            "score": audit['score'],
            "re_teaching": new_explanation, 
            "feedback": audit['feedback']
        }
    
    os.remove(temp_audio)
    return response

# --- RUNNER ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)