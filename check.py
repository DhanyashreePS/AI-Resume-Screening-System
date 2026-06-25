from utils.tfidf_matcher import calculate_similarity

resume = """
Python developer with Flask, SQL and REST APIs.
"""

job_description = """
Looking for a Python backend developer with database skills.
"""

score = calculate_similarity(
    resume,
    job_description
)

print("Similarity Score:", score)