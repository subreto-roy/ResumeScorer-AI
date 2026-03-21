
import json

def score_cv(cv_data, readable_file="skills.json"):
    """
    cv_data: {'name','email','phone','skills','experience'}
    readable_file: JSON with required skills & weights
    """
    with open(readable_file, 'r') as f:
        required_skills = json.load(f)  # e.g. {"Python":10,"Django":10,"ML":15}

    skills_found = cv_data.get("skills", [])
    score = sum([required_skills.get(skill,0) for skill in skills_found])
    return score