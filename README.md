## 🧠 Mastery-Mind: Bloom's-Powered Autonomous Learning
Team: Nirupathunga (Lead), Krishnakanth, Kamaleshwaran

Institution: Sri Ramakrishna Institute of Technology (SRIT)

Event: GRASP 2026

## 🚀 The Vision
Most educational tools focus on Rote Learning—memorizing facts to pass a test. Mastery-Mind is a Closed-Loop Adaptive System that ensures a student truly understands a concept before moving forward. By combining GPT-4o’s reasoning with Deepgram’s voice analysis, we force Active Recall and Synthesis.

## ✨ Key Features
📋 Syllabus-to-Bloom Mapping
Upload any PDF or image of notes. We use PyMuPDF4LLM and Tesseract to extract content and GPT-4o to map it into Bloom's Taxonomy levels (Recall ➔ Apply ➔ Synthesize).

🎙️ "Explain-Back" Voice Audit
Students record their explanation of a topic. Deepgram Nova-3 transcribes the audio, and our AI auditor checks for logical reasoning gaps rather than just keywords.

🔄 Adaptive Re-Teaching
If the mastery score is below 80%, the AI re-teaches the concept using a new analogy specifically targeting the student's identified misunderstanding.

📅 1-4-7 Day Autonomous Retention
Using APScheduler, we schedule nudges for Day 1, Day 4, and Day 7 after a topic is mastered to ensure long-term memory retention.

## 🛠️ Technology Stack
⚡ Backend Framework: FastAPI
Chosen for high performance and native async support, allowing us to process large audio and PDF files without blocking the server.

🧠 Reasoning Engine: OpenAI GPT-4o
Used for complex Bloom's Taxonomy mapping and identifying nuanced logical fallacies in student explanations.

🗣️ Voice Processing: Deepgram Nova-3
Selected to ensure Linguistic Fairness. It handles Indian accents and "Hinglish" perfectly, ensuring students aren't penalized for how they speak, but only for what they understand.

📄 Content Extraction: PyMuPDF4LLM & Tesseract
Provides clean Markdown extraction from digital PDFs and high-accuracy OCR for handwritten textbook notes.

⏰ Job Scheduler: APScheduler
Manages the persistent 1-4-7 day background notifications even if the server restarts.

## 📊 System Architecture
  graph TD
    A[Syllabus Upload: PDF/Image] --> B[PyMuPDF4LLM/Tesseract]
    B --> C[GPT-4o: Bloom's Taxonomy Mapping]
    C --> D[Dynamic Topic Explanation]
    D --> E[Voice Explain-Back Recording]
    E --> F[Deepgram: Accents-Aware Transcription]
    F --> G[GPT-4o: Reasoning Audit]
    G -- Score < 80 --> H[Adaptive Re-Teaching Loop]
    H --> D
    G -- Score >= 80 --> I[Mastery Achieved]
    I --> J[APScheduler: 1-4-7 Day Nudges]

## 🚦 How to Run
1. Clone & Setup
git clone https://github.com/[your-username]/GRASP-2026-Mastery-EdTech.git
cd GRASP-2026-Mastery-EdTech
2. Install Dependencies
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
export DEEPGRAM_API_KEY="your_key"
3. Launch
python3 -m uvicorn main:app --reload

Access the API documentation at http://localhost:8000/docs.
