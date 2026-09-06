"""Geheimnis-Maskierung."""


def mask_secret(text: str, keep: int = 4) -> str:
    """Maskiere *text* und lasse höchstens die letzten *keep* Zeichen sichtbar.

    Bei ``len(text) > keep`` bleiben die letzten *keep* Zeichen erhalten und alle
    vorangehenden werden durch ``'*'`` ersetzt (Gesamtlänge unverändert). Bei
    ``len(text) <= keep`` werden ausschließlich ``'*'`` in der Länge des Texts
    zurückgegeben — niemals ein Originalzeichen.
    """
    if not isinstance(text, str):
        raise TypeError("text muss ein str sein")
    if not isinstance(keep, int):
        raise TypeError("keep muss ein int sein")
    if keep < 0:
        raise ValueError("keep darf nicht negativ sein")

    if keep == 0 or len(text) <= keep:
        return "*" * len(text)
    return "*" * (len(text) - keep) + text[-keep:]
