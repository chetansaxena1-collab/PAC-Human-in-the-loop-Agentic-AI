"""Small UI matching helpers for guided Streamlit selectors."""
from __future__ import annotations

import re
from rapidfuzz import fuzz
FUZZY_MATCH_THRESHOLD = 90

QUERY_STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "i",
    "in",
    "is",
    "need",
    "please",
    "the",
    "to",
    "change",
    "modify",
    "update",
    "want",
    "wnat",
    "would",
    "can",
    "could",
    "should",
    "help",
    "me",
    "my",
    "our",
    "this",
    "that",
    "from",
    "with",
    "using",
}

QUERY_SYNONYMS = {
    "analysis": {"test", "procedure"},
    "analyses": {"test", "procedure"},
    "analytical": {"test", "procedure"},
    "assay": {"test", "procedure"},
    "method": {"test", "procedure"},
    "methods": {"test", "procedure"},
    "validation": {"test", "procedure"},
    "plant": {"manufacturing", "site"},
    "manufacturer": {"manufacturing", "site"},
    "facility": {"manufacturing", "site"},
    "location": {"manufacturing", "site"},
    "batch": {"batch", "release"},
    "supplier": {"supplier"},
    "source": {"supplier"},
    "addition": {"addition"},
    "add": {"addition"},
    "new": {"addition"},
    "deletion": {"deletion"},
    "remove": {"deletion"},
    "eliminate": {"deletion"},
    # Manufacturing
    "site": {"site", "manufacturing", "facility", "plant", "location"},
    "factory": {"manufacturing", "facility", "site"},
    "factory site": {"manufacturing", "site"},
    "production": {"manufacturing"},
    "production site": {"manufacturing", "site"},

    # Testing
    "laboratory": {"testing", "site"},
    "qc": {"quality", "control", "testing"},
    "quality control": {"testing"},
    "quality": {"testing"},

    # Batch Release
    "batch release": {"batch", "release"},
    "release": {"batch", "release"},
    "release facility": {"batch", "release", "site"},

    # Suppliers
    "vendor": {"supplier"},
    "manufacturer supplier": {"supplier"},
    "contract manufacturer": {"manufacturing", "site"},
}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", str(text or "").casefold())


def _meaningful_query_terms(query: str) -> list[str]:
    terms = [token for token in _tokens(query) if token not in QUERY_STOPWORDS]
    expanded_terms = set()
    for term in terms:
        expanded_terms.update(QUERY_SYNONYMS.get(term, {term}))
    return sorted(expanded_terms)


def _token_matches(query_term: str, option_token: str) -> bool:
    if query_term == option_token:
        return True
    if len(query_term) >= 3 and option_token.startswith(query_term):
        return True
    
    # RapidFuzz similarity
    if fuzz.WRatio(query_term, option_token) >= FUZZY_MATCH_THRESHOLD:
        return True
    
    return False


def _option_match_score(option: str, query_terms: list[str]) -> tuple[int, int, str]:
    option_tokens = _tokens(option)
    matched_terms = sum(
        1
        for term in query_terms
        if any(_token_matches(term, option_token) for option_token in option_tokens)
    )
    exact_phrase_bonus = 1 if " ".join(query_terms) in " ".join(option_tokens) else 0
    return matched_terms, exact_phrase_bonus, str(option).casefold()


def _direct_match_count(option: str, query: str) -> int:
    option_tokens = _tokens(option)
    return sum(
        1
        for term in _tokens(query)
        if term not in QUERY_STOPWORDS
        and any(_token_matches(term, option_token) for option_token in option_tokens)
    )


def filter_options_by_query(
    options: list[str],
    query: str,
) -> list[str]:
    query_terms = _meaningful_query_terms(query)
    if not query_terms:
        return []

    scored_options = [
        (_option_match_score(option, query_terms), option)
        for option in options
    ]
    matches = [
        (score, option)
        for score, option in scored_options
        if score[0] == len(query_terms)
    ]
    if not matches:
        matches = [
            (score, option)
            for score, option in scored_options
            if score[0] >= 2 and _direct_match_count(option, query) >= 1
        ]
    return [
        option
        for _, option in sorted(matches, key=lambda scored: (-scored[0][1], scored[0][2]))
    ]
