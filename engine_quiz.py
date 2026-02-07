def generate_mastery_quiz(syllabus_text):
    prompt = f"""
    Based on this text: {syllabus_text}
    Generate 3 'Synthesis' level Multiple Choice Questions.
    Format strictly as JSON:
    {{
      "quiz": [
        {{"q": "...", "options": ["A", "B", "C"], "correct": "A", "rationale": "..."}}
      ]
    }}
    """
    # Use your existing engine_brain.py logic to call OpenAI
    # return get_json_from_gpt(prompt)