# validkit

Eine kleine, eigenständige Python-Bibliothek, die mehrere unabhängige, reine
Prüf- und Normalisierungsfunktionen bereitstellt: E-Mail-Validierung,
Luhn-Prüfung, IBAN-Modulo-97-Prüfung, ISBN-13-Prüfung, Telefonnormalisierung
nach E.164, Akzent-Entfernung, Geheimnis-Maskierung, Slug-Erzeugung und
Werte-Clamping. Jede Funktion ist sauber typannotiert, bei ungültigen Eingaben
mit aussagekräftigen Fehlern versehen und einzeln nutzbar.

## Tech-Stack

- **Sprache**: Python 3 (requires-python `>=3.9`)
- **Abhängigkeiten**: nur Python-Standardbibliothek — keine Laufzeit-Dependencies
- **Tests**: pytest
- **Projekttyp**: `python-backend` (reine Bibliothek, ohne CLI, ohne Netzwerk)

## Installation

```bash
pip install -e .
```

## Tests ausführen

```bash
pytest
```

## Verwendung

Alle neun Funktionen werden über `validkit` exportiert:

```python
import validkit

validkit.is_valid_email("a@b.co")  # -> True
validkit.luhn_check("79927398713")  # -> True
validkit.is_valid_iban("DE89 3704 0044 0532 0130 00")  # -> True
validkit.is_valid_isbn13("9780306406157")  # -> True
validkit.normalize_phone("(030) 1234-567", "DE")  # -> "+49301234567"
validkit.strip_accents("café")  # -> "cafe"
validkit.mask_secret("geheim1234")  # -> maskiert, endet auf "1234"
validkit.slugify("Héllo Wörld!")  # -> "hello-world"
validkit.clamp(5, 0, 10)  # -> 5
```

## Funktionen

| Funktion | Signatur | Beschreibung |
| --- | --- | --- |
| `is_valid_email` | `(text: str) -> bool` | Prüft, ob `text` eine gültige E-Mail-Adresse ist. |
| `luhn_check` | `(digits: str) -> bool` | Prüft eine Ziffernfolge gegen den Luhn-Algorithmus. |
| `is_valid_iban` | `(text: str) -> bool` | Prüft eine IBAN per Modulo-97 (Leerzeichen erlaubt). |
| `is_valid_isbn13` | `(text: str) -> bool` | Prüft eine ISBN-13 inklusive Prüfziffer. |
| `normalize_phone` | `(text: str, country_code: str) -> str` | Normalisiert eine Telefonnummer nach E.164. |
| `strip_accents` | `(text: str) -> str` | Entfernt diakritische Zeichen. |
| `mask_secret` | `(text: str, keep: int = 4) -> str` | Maskiert ein Geheimnis; höchstens die letzten `keep` Zeichen bleiben sichtbar. |
| `slugify` | `(text: str) -> str` | Erzeugt einen kleingeschriebenen, trennzeichenbasierten Slug. |
| `clamp` | `(value: float, low: float, high: float) -> float` | Begrenzt `value` auf `[low, high]`. |
