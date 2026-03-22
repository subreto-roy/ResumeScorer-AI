import os
import json
import re
import pdfplumber
import docx
from groq import Groq


def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF or DOCX file."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    elif ext in ['.docx', '.doc']:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()

    return ""


def analyze_cv_with_grok(reference_text: str, candidate_text: str) -> dict:
    """Use Groq AI to compare candidate CV with reference CV."""

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
You are an expert HR analyst. Compare the CANDIDATE CV against the REFERENCE CV and provide a detailed matching analysis.

REFERENCE CV:
{reference_text[:3000]}

CANDIDATE CV:
{candidate_text[:3000]}

Analyze and return ONLY a valid JSON object (no markdown, no explanation, no code fences) with this exact structure:
{{
    "overall_score": <number 0-100>,
    "skills_score": <number 0-100>,
    "experience_score": <number 0-100>,
    "education_score": <number 0-100>,
    "keywords_score": <number 0-100>,
    "candidate_name": "<extracted name or 'Unknown'>",
    "matched_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "summary": "<2-3 sentence overall assessment>"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert HR analyst. Always respond with valid JSON only, no markdown, no code fences."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.3,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if present
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    return json.loads(raw)