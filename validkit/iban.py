"""IBAN-Prüfung (Modulo-97) nach ISO 13616."""

_MAX_LENGTH = 1000
_MIN_LENGTH = 15


def is_valid_iban(text: str) -> bool:
    """Prüfe, ob *text* eine gültige IBAN ist (Modulo-97-Prüfung)."""
    if not isinstance(text, str):
        raise TypeError("input must be a string")
    if len(text) > _MAX_LENGTH:
        raise ValueError("input exceeds maximum length of 1000 characters")

    stripped = text.replace(" ", "").upper()

    if not stripped.isalnum():
        raise ValueError("input must be alphanumeric after removing spaces")
    if len(stripped) < _MIN_LENGTH:
        raise ValueError("input is too short to be a valid IBAN")

    rearranged = stripped[4:] + stripped[:4]

    digits = "".join(str(ord(ch) - ord("A") + 10) if ch.isalpha() else ch for ch in rearranged)

    return int(digits) % 97 == 1
