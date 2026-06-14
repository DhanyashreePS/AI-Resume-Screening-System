def calculate_match(candidate_skills, required_skills):

    candidate_set = set(skill.lower() for skill in candidate_skills)

    required_set = set(skill.lower() for skill in required_skills)

    matched_skills = list(candidate_set.intersection(required_set))

    missing_skills = list(required_set - candidate_set)

    if len(required_set) == 0:
        score = 0
    else:
        score = round(
            (len(matched_skills) / len(required_set)) * 100,
            2
        )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }