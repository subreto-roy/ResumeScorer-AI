from .services.extractor import extract_text
from .services.cleaner import clean_text
from .services.grok_parser import parse_with_grok

def parse_cv(file_path):
    text = extract_text(file_path)
    clean = clean_text(text)
    return parse_with_grok(clean)

def calculate_match_score(uploaded_cv, reference_cv):
    """
    Simple skill + experience match
    uploaded_cv & reference_cv are parsed_data dicts
    """
    score = 0
    total = 0

    # ---- Skill match ----
    uploaded_skills = set([s.lower() for s in uploaded_cv.get("skills", [])])
    reference_skills = set([s.lower() for s in reference_cv.get("skills", [])])
    if reference_skills:
        matched = uploaded_skills & reference_skills
        skill_score = len(matched) / len(reference_skills) * 50  # 50% weight
    else:
        skill_score = 0

    # ---- Experience match ----
    uploaded_exp_roles = set([exp.get("role", "").lower() for exp in uploaded_cv.get("experience", [])])
    reference_exp_roles = set([exp.get("role", "").lower() for exp in reference_cv.get("experience", [])])
    if reference_exp_roles:
        matched_exp = uploaded_exp_roles & reference_exp_roles
        exp_score = len(matched_exp) / len(reference_exp_roles) * 50  # 50% weight
    else:
        exp_score = 0

    score = skill_score + exp_score
    return round(score, 2)