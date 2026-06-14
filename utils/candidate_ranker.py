def rank_candidates(candidates):

    ranked_candidates = sorted(
        candidates,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_candidates