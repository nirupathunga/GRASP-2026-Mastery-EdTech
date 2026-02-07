import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Groq Client Setup
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"

def get_blooms_assessment(md_text: str):
    """
    Analyzes the syllabus and maps topics to Bloom's Taxonomy.
    """
    prompt = f"""
    Analyze the following syllabus text and extract the main topics. 
    For each topic, assign a Bloom's Taxonomy level (Remember, Understand, Apply, Analyze, Evaluate, Create).
    Return the result ONLY as a JSON object with a key 'topics' containing a list of objects with 'title' and 'level'.
    
    Syllabus:
    {md_text}
    """
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def audit_reasoning(topic, transcript):
    # Your existing audit code...
    return {"score": 85, "feedback": "Good understanding.", "status": "Mastered!"}

def get_adaptive_instruction(gap_details):
    # Your existing adaptive instruction code...
    return "Think of it like a library system..."