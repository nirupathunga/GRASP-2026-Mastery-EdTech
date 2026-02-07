import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_blooms_assessment(content: str):
    prompt = f"""
    Analyze the following academic content and generate:
    1. A summary mapped to Bloom's Taxonomy.
    2. One 'Application' level question (Scenario-based).
    3. One 'Synthesis' level challenge (Combine ideas).
    
    Content: {content}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
