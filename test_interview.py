from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.interview_generator import generate_questions

text = extract_text_from_pdf(
    "resumes/dhanya-resume.pdf"
)

skills = extract_skills(text)

questions = generate_questions(skills)

for skill, q_list in questions.items():

    print(f"\n{skill.upper()} QUESTIONS")

    for i, question in enumerate(q_list, start=1):
        print(f"{i}. {question}")