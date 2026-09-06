"""Luhn-Prüfzifferprüfung."""


def luhn_check(digits: str) -> bool:
    """Prüfe eine Ziffernfolge gegen den Luhn-Algorithmus (Mod-10)."""
    if not isinstance(digits, str):
        raise TypeError("digits must be a string")
    if not digits:
        raise ValueError("digits must not be empty")
    if not digits.isascii() or not digits.isdigit():
        raise ValueError("digits must contain only ASCII digits")

    total = 0
    for index, char in enumerate(reversed(digits)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value

    return total % 10 == 0
