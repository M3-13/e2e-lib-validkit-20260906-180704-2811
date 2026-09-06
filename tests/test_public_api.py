"""Öffentliche API: Importierbarkeit und Signaturen (nur Skeleton)."""

import inspect

import pytest

import validkit

# name -> (parameter names, parameter annotations, return annotation)
CASES = {
    "is_valid_email": (["text"], [str], bool),
    "luhn_check": (["digits"], [str], bool),
    "is_valid_iban": (["text"], [str], bool),
    "is_valid_isbn13": (["text"], [str], bool),
    "normalize_phone": (["text", "country_code"], [str, str], str),
    "strip_accents": (["text"], [str], str),
    "mask_secret": (["text", "keep"], [str, int], str),
    "slugify": (["text"], [str], str),
    "clamp": (["value", "low", "high"], [float, float, float], float),
}


def test_version_exported():
    assert validkit.__version__ == "0.1.0"
    assert "__version__" in validkit.__all__


@pytest.mark.parametrize("name", sorted(CASES))
def test_all_public_names_importable(name):
    assert name in validkit.__all__
    assert callable(getattr(validkit, name))


@pytest.mark.parametrize("name", sorted(CASES))
def test_signature(name):
    func = getattr(validkit, name)
    sig = inspect.signature(func)
    param_names, annotations, return_annotation = CASES[name]
    assert list(sig.parameters) == param_names
    for i, param_name in enumerate(param_names):
        assert sig.parameters[param_name].annotation is annotations[i]
    assert sig.return_annotation is return_annotation


def test_mask_secret_default_keep():
    sig = inspect.signature(validkit.mask_secret)
    assert sig.parameters["keep"].default == 4
