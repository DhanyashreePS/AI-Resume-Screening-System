from utils.candidate_ranker import rank_candidates

candidates = [
    {"name": "Dhanya", "score": 85},
    {"name": "Rahul", "score": 70},
    {"name": "Priya", "score": 92}
]

ranked = rank_candidates(candidates)

print("\nCandidate Ranking")
print("------------------------")

for rank, candidate in enumerate(ranked, start=1):
    print(
        f"{rank}. {candidate['name']} - {candidate['score']}%"
    )