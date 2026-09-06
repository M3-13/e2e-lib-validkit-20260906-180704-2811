"""Slug-Erzeugung."""

import re
import unicodedata

_MAX_LENGTH = 1000

_NON_WORD_RE = re.compile(r"[^a-z0-9_]+")


def slugify(text: str) -> str:
    """Erzeuge aus *text* einen kleingeschriebenen, trennzeichenbasierten Slug."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > _MAX_LENGTH:
        raise ValueError(f"text exceeds maximum length of {_MAX_LENGTH} characters")

    normalized = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in normalized if not unicodedata.combining(c))
    lowered = ascii_only.lower()
    replaced = _NON_WORD_RE.sub("-", lowered)
    return replaced.strip("-")
