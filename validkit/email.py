"""E-Mail-Validierung."""

_LOCAL_ALLOWED = ".-_+"
_DOMAIN_ALLOWED = ".-"


def is_valid_email(text: str) -> bool:
    """Prüfe *text* syntaktisch als E-Mail-Adresse.

    Rein syntaktische Prüfung: erlaubte Zeichen und Struktur von lokalem Teil
    und Domain. Ein ungültiges Format ergibt ``False`` (kein Fehler).
    """
    if not isinstance(text, str):
        raise TypeError("text muss ein str sein")
    if len(text) > 1000:
        raise ValueError("text ist länger als 1000 Zeichen")

    if text.count("@") != 1:
        return False
    local, domain = text.split("@")

    if not local or not domain:
        return False

    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    for char in local:
        if not (char.isalnum() or char in _LOCAL_ALLOWED):
            return False

    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    if "." not in domain:
        return False
    for char in domain:
        if not (char.isalnum() or char in _DOMAIN_ALLOWED):
            return False

    tld = domain.rsplit(".", 1)[1]
    return not tld.isdigit()
