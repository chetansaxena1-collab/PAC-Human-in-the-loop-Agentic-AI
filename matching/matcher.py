"""
Main regulatory matching workflow.

Pipeline

1. Normalize input
2. Apply synonym mapping
3. Exact match
4. RapidFuzz suggestion
"""

from matching.normalizer import normalize_text
from matching.synonyms import apply_synonyms
from matching.fuzzy_match import get_best_matches


def find_regulatory_match(
    user_input: str,
    regulatory_phrases: list[str],
):
    """
    Find the best regulatory match.

    Returns
    -------
    {
        "match": str | None,
        "suggestions": list
    }
    """

    # -----------------------------
    # Level 1
    # Normalize
    # -----------------------------
    normalized_input = normalize_text(user_input)

    normalized_phrases = {
        normalize_text(item): item
        for item in regulatory_phrases
    }

    # -----------------------------
    # Level 2
    # Synonyms
    # -----------------------------
    synonym_input = apply_synonyms(normalized_input)

    # -----------------------------
    # Exact Match
    # -----------------------------
    if synonym_input in normalized_phrases:

        return {
            "match": normalized_phrases[synonym_input],
            "suggestions": [],
        }

    # -----------------------------
    # Level 3
    # RapidFuzz
    # -----------------------------
    suggestions = get_best_matches(
        synonym_input,
        list(normalized_phrases.keys()),
        limit=3,
    )

    formatted = []

    for phrase, score, _ in suggestions:

        if score >= 85:

            formatted.append(
                {
                    "phrase": normalized_phrases[phrase],
                    "score": score,
                }
            )

    return {
        "match": None,
        "suggestions": formatted,
    }