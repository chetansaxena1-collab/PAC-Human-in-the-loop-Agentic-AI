"""
RapidFuzz helper functions.

Provides similarity-based matching
without changing the original workbook.
"""

from rapidfuzz import process
from rapidfuzz import fuzz


def get_best_matches(
    query: str,
    choices: list[str],
    limit: int = 3,
):
    """
    Return the top matching regulatory phrases.
    """

    return process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        limit=limit,
    )