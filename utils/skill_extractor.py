SKILLS_DB = [
    "python",
    "java",
    "sql",
    "django",
    "flask",
    "machine learning",
    "deep learning",
    "html",
    "css",
    "javascript",
    "mysql",
    "mongodb",
    "git",
    "github",
    "data structures",
    "c",
    "c++"
]


def extract_skills(resume_text):
    detected_skills = []

    resume_text = resume_text.lower()

    for skill in SKILLS_DB:
        if skill.lower() in resume_text:
            detected_skills.append(skill)

    return list(set(detected_skills))