from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.candidate_extractor import (
    extract_name,
    extract_email,
    extract_phone
)
from utils.job_matcher import calculate_match
resume_path = "resumes/dhanya-resume.pdf"

text = extract_text_from_pdf(resume_path)

skills = extract_skills(text)

name = extract_name(text)
email = extract_email(text)
phone = extract_phone(text)

print("\nCandidate Details")
print("------------------")
print("Name :", name)
print("Email:", email)
print("Phone:", phone)

print("\nDetected Skills")
print("------------------")

for skill in skills:
    print(skill)

required_skills = [
    "python",
    "sql",
    "django",
    "git",
    "html",
    "css",
    "machine learning"
]

result = calculate_match(skills, required_skills)

print("\nJob Match Report")
print("------------------")

print("Match Score:", result["score"], "%")

print("\nMatched Skills:")
for skill in result["matched_skills"]:
    print("-", skill)

print("\nMissing Skills:")
for skill in result["missing_skills"]:
    print("-", skill)