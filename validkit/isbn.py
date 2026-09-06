"""ISBN-13-Prüfung."""


def is_valid_isbn13(text: str) -> bool:
    """Prüfe, ob *text* eine gültige ISBN-13 ist.

    Bindestriche und Leerzeichen werden entfernt; danach müssen exakt 13
    Ziffern übrig bleiben, sonst wird ``ValueError`` ausgelöst. Die
    Prüfziffer wird über alternierende Gewichte 1 und 3 (erste Ziffer
    Gewicht 1) kontrolliert.
    """
    if not isinstance(text, str):
        raise TypeError("text muss ein str sein")
    if len(text) > 1000:
        raise ValueError("Eingabe zu lang (max. 1000 Zeichen)")

    digits = text.replace("-", "").replace(" ", "")

    if not digits.isdigit():
        raise ValueError("ISBN darf nur Ziffern, Bindestriche und Leerzeichen enthalten")
    if len(digits) != 13:
        raise ValueError("ISBN-13 muss genau 13 Ziffern haben")

    total = 0
    for i, ch in enumerate(digits):
        weight = 1 if i % 2 == 0 else 3
        total += int(ch) * weight

    return total % 10 == 0
