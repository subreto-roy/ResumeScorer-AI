import os
import requests

# API key secret ভাবে রাখো, direct code-এ লিখবে না
GROK_API_KEY = os.getenv("GROK_API_KEY")  # .env file or system env
GROK_API_URL = "https://api.x.ai/v1/chat/completions"  # Official endpoint

def parse_cv_grok(file_path):
    """
    Parses a CV file (PDF/DOCX/TXT) using Grok API
    Returns structured info: name, email, phone, skills, experience
    """
    with open(file_path, 'rb') as f:
        cv_text = f.read().decode(errors="ignore")  # Read file as text
    
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-4-1-fast",
        "messages": [
            {"role": "system", "content": "You are a CV parsing assistant. Extract structured information like name, email, phone, skills, and experience."},
            {"role": "user", "content": cv_text}
        ],
        "temperature": 0,
        "stream": False
    }

    response = requests.post(GROK_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # raise error if request failed

    data = response.json()
    # Extract assistant's reply
    assistant_text = data['choices'][0]['message']['content']

    # Optional: parse assistant_text as JSON if Grok returns structured JSON
    try:
        import json
        structured_data = json.loads(assistant_text)
    except:
        # fallback if not valid JSON
        structured_data = {
            "raw_text": assistant_text
        }

    return structured_data

# Example usage
if __name__ == "__main__":
    result = parse_cv_grok("cvs/sample_cv.pdf")
    print(result)