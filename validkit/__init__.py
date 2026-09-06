"""validkit — Prüf- und Normalisierungsfunktionen.

Eine kleine, eigenständige Python-Bibliothek (nur Standardbibliothek), die
mehrere unabhängige, reine Prüf- und Normalisierungsfunktionen bereitstellt.
"""

from .accents import strip_accents
from .clamp import clamp
from .email import is_valid_email
from .iban import is_valid_iban
from .isbn import is_valid_isbn13
from .luhn import luhn_check
from .masking import mask_secret
from .phone import normalize_phone
from .slugify import slugify

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "clamp",
    "is_valid_email",
    "is_valid_iban",
    "is_valid_isbn13",
    "luhn_check",
    "mask_secret",
    "normalize_phone",
    "slugify",
    "strip_accents",
]
