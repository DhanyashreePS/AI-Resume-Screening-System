QUESTION_BANK = {
    "python": [
        "What is inheritance in Python?",
        "What is a decorator?",
        "Difference between list and tuple?",
        "What is exception handling?"
    ],

    "sql": [
        "What is a JOIN?",
        "Difference between WHERE and HAVING?",
        "What is normalization?",
        "What is a primary key?"
    ],

    "django": [
        "Explain MVT architecture.",
        "What are Models in Django?",
        "What is a migration?",
        "What is Django ORM?"
    ],

    "html": [
        "What is semantic HTML?",
        "Difference between div and span?"
    ],

    "css": [
        "What is Flexbox?",
        "Difference between relative and absolute positioning?"
    ],

    "javascript": [
        "What is a closure?",
        "Difference between var, let and const?"
    ],

    "machine learning": [
        "What is overfitting?",
        "Difference between supervised and unsupervised learning?",
        "What is cross-validation?"
    ]
}


def generate_questions(skills):
    questions = {}

    for skill in skills:
        skill = skill.lower()

        if skill in QUESTION_BANK:
            questions[skill] = QUESTION_BANK[skill]

    return questions