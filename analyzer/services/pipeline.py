
from .grok_parser import parse_cv_grok
from .scoring import score_cv

def process_cv(file_path, readable_file="skills.json"):
    cv_data = parse_cv_grok(file_path)
    score = score_cv(cv_data, readable_file)
    cv_data['score'] = score
    return cv_data

# Example
if __name__ == "__main__":
    cv = process_cv("cvs/sample_cv.pdf")
    print(cv)