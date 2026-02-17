from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Naya Client initialize karein
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_document(file_content):
    prompt = f"""
    Analyze this document for AI Employee Vault.
    Return a JSON with:
    - decision: "Approved" or "Rejected"
    - confidence: 0.0 to 1.0
    - reasoning: brief explanation
    
    Document: {file_content}
    """

    try:
        # Naya SDK method: models.generate_content
        response = client.models.generate_content(
            model="models/gemini-2.5-flash", 
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        # Naye SDK mein response.text direct milta hai
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini Brain Error: {e}")
        return {"decision": "Rejected", "confidence": 0, "reasoning": "Technical Error"}