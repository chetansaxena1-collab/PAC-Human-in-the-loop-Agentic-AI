"""
Regulatory synonym mapping.

This module standardizes commonly used user phrases
to the preferred regulatory terminology.
"""

from matching.normalizer import normalize_text


# Add more synonyms here whenever required.
SYNONYM_MAP = {

    # Manufacturing Site
    "site addition": "addition of a manufacturing site",
    "new site": "addition of a manufacturing site",
    "new manufacturing site": "addition of a manufacturing site",
    "manufacturing location": "manufacturing site",
    "manufacturer": "manufacturing site",

    # Batch Release
    "release site": "batch release site",
    "batch release location": "batch release site",

    # Testing
    "testing laboratory": "testing site",
    "testing lab": "testing site",
    "lab": "testing site",

    # Supplier
    "new supplier": "addition of a supplier",
    "supplier change": "change in supplier",

}


def apply_synonyms(text: str) -> str:
    """
    Replace known user phrases with standard regulatory terminology.
    """

    normalized = normalize_text(text)

    return SYNONYM_MAP.get(normalized, normalized)