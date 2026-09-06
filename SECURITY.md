VERDICT: CHANGES_REQUESTED

## Zusammenfassung

Die Bibliothek `validkit` ist eine kleine, eigenständige Python-Bibliothek ohne Netzwerk-, CLI- oder UI-Anteil. Es wurden keine hartkodierten Secrets, keine Codeausführungs-/Deserialisierungskonstrukte und keine unsicheren Abhängigkeiten gefunden. Die geforderten Längengrenzen und die Geheimnismaskierung gemäß AC-11/AC-12/AC-15 sind weitgehend korrekt umgesetzt.

Die verbleibenden Befunde betreffen überwiegend die Eingabevalidierung: Mehrere Prüffunktionen akzeptieren Unicode-Ziffern bzw. Unicode-Buchstaben, obwohl die jeweiligen Formate (E.164, ISBN-13, IBAN) ausschließlich ASCII-Zeichen vorsehen. Dadurch können formal ungültige Eingaben als gültig durchgehen oder fehlerhaft normalisiert werden. Außerdem fehlt in `luhn_check` eine Längenbegrenzung, und `mask_secret` akzeptiert den Wahrheitswert `bool` als `keep`-Parameter.

## Scanner-Abdeckung

- **bandit**: `[skipped] bandit not installed` — keine Ergebnisse.
- **semgrep**: `[skipped] semgrep not installed` — keine Ergebnisse.

Aus den ausgefallenen Scans können keine Befunde abgeleitet werden; die folgenden Punkte beruhen ausschließlich auf der manuellen Codeanalyse.

## Befunde

### 1. Low — Unicode-Ziffern in `normalize_phone` werden akzeptiert
**Betroffene Stelle:** `validkit/phone.py`, Zeile mit `digits = "".join(...)` und `if not digits or not digits.isdigit():`

`str.isdigit()` liefert auch für Unicode-Ziffern wie arabisch-indische Ziffern `١٢٣` den Wert `True`. Die Funktion gibt in diesem Fall eine nicht E.164-konforme Zeichenkette wie `"+49١٢٣٤٥٦"` zurück, statt die Nummer als ungültig abzulehnen.

**Fix:**
```python
if not digits or not digits.isascii() or not digits.isdigit():
    raise ValueError("invalid phone number")
```
oder alternativ:
```python
if not digits or any(ch not in "0123456789" for ch in digits):
    raise ValueError("invalid phone number")
```

### 2. Low — Unicode-Ziffern in `is_valid_isbn13` werden akzeptiert
**Betroffene Stelle:** `validkit/isbn.py`, nach `digits = text.replace("-", "").replace(" ", "")`

Dasselbe Problem wie bei der Telefonnormalisierung: `digits.isdigit()` akzeptiert Unicode-Ziffern, eine ISBN-13 besteht jedoch ausschließlich aus ASCII-Ziffern. Ein Aufrufer kann dadurch formal ungültige Identifikatoren als gültig einstufen.

**Fix:**
```python
if not digits.isascii() or not digits.isdigit():
    raise ValueError("ISBN darf nur ASCII-Ziffern, Bindestriche und Leerzeichen enthalten")
```

### 3. Low — Unicode-alphanumerische Zeichen in `is_valid_iban` möglich
**Betroffene Stelle:** `validkit/iban.py`, nach `stripped = text.replace(" ", "").upper()`

`stripped.isalnum()` erlaubt Unicode-Buchstaben und Unicode-Ziffern. Da später `ch.isalpha()` verwendet wird, werden Unicode-Buchstaben in unerwartete Zahlenwerte umgewandelt und die Modulo-97-Prüfung läuft auf einer falschen Grundlage. Eine IBAN darf laut ISO 13616 nur die ASCII-Zeichen `A–Z` und `0–9` enthalten.

**Fix:**
```python
if not stripped.isascii() or not stripped.isalnum():
    raise ValueError("input must contain only ASCII letters and digits after removing spaces")
```
oder mit regulärem Ausdruck:
```python
if not re.fullmatch(r"[A-Z0-9]+", stripped):
    raise ValueError("input must contain only ASCII letters and digits")
```

### 4. Low — `luhn_check` ohne Längenbegrenzung
**Betroffene Stelle:** `validkit/luhn.py`, vor der Zeichenschleife

Die Spezifikation AC-11 nennt `luhn_check` nicht explizit, dennoch handelt es sich um eine Textverarbeitungsfunktion, die direkt über einen String iteriert und `int()` pro Zeichen aufruft. Sehr lange Eingaben können unnötig viel Rechenzeit verbrauchen. Eine einheitliche Begrenzung auf 1000 Zeichen wäre konsistent mit den übrigen Funktionen und schützt vor versehentlich sehr großen Eingaben.

**Fix:**
```python
if not digits.isascii() or not digits.isdigit():
    raise ValueError("digits must contain only ASCII digits")
if len(digits) > 1000:
    raise ValueError("input exceeds maximum length of 1000 characters")
```

### 5. Low — `mask_secret` akzeptiert `bool` als `keep`
**Betroffene Stelle:** `validkit/masking.py`, Typprüfung von `keep`

In Python ist `bool` eine Unterklasse von `int`. Dadurch wird `mask_secret("abcd", True)` nicht als Typfehler abgewiesen, sondern `True` als `1` interpretiert und liefert `"***d"`. Das widerspricht der Erwartung, dass `keep` eine echte Ganzzahl sein muss.

**Fix:**
```python
if isinstance(keep, bool) or not isinstance(keep, int):
    raise TypeError("keep muss ein int sein")
```

## Nicht beanstandet

- **Secrets:** Keine hartkodierten Schlüssel, Passwörter oder Token. Die `.gitignore` schließt typische Secret-Dateien aus.
- **Injection/RCE:** Keine Verwendung von `eval`, `exec`, `pickle`, `subprocess`, `os.system` o. Ä.; ausschließlich Standardbibliotheksimporte.
- **AuthN/AuthZ:** Nicht zutreffend, keine Dienste oder Sitzungen.
- **Dependencies:** Keine Laufzeitabhängigkeiten. Das Build-System benötigt nur `setuptools`.
- **Fehlermeldungen:** Enthalten keine Eingabedaten und entsprechen damit den Datenschutz-Anforderungen AC-14/AC-15.
- **Maskierung:** `mask_secret` erfüllt AC-12/AC-15, sobald der `bool`-Fall bereinigt ist.