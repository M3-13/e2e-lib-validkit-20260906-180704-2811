"""Akzent-Entfernung."""

import unicodedata


def strip_accents(text: str) -> str:
    """Entferne diakritische Zeichen aus *text*."""
    if not isinstance(text, str):
        raise TypeError("expected a string")
    if len(text) > 1000:
        raise ValueError("input exceeds 1000 characters")

    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if unicodedata.combining(ch) == 0)
