"""Telefonnormalisierung nach E.164."""

_COUNTRY_CODES = {
    "DE": "49",
    "AT": "43",
    "CH": "41",
    "US": "1",
    "GB": "44",
    "FR": "33",
    "NL": "31",
    "IT": "39",
    "ES": "34",
}

_MAX_LENGTH = 1000

_REMOVABLE_FORMAT = "() -."


def normalize_phone(text: str, country_code: str) -> str:
    """Normalisiere *text* für *country_code* zu einer E.164-Nummer."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(country_code, str):
        raise TypeError("country_code must be a string")

    if len(text) > _MAX_LENGTH:
        raise ValueError("input too long")

    country_number = _COUNTRY_CODES.get(country_code)
    if country_number is None:
        raise ValueError("unknown country code")

    digits = "".join(ch for ch in text if ch not in _REMOVABLE_FORMAT)

    if not digits or not digits.isdigit():
        raise ValueError("invalid phone number")

    if digits.startswith("0"):
        digits = digits[1:]

    if len(digits) < 6:
        raise ValueError("invalid phone number")

    return "+" + country_number + digits
