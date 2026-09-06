"""Tests für slugify."""

import pytest

from validkit.slugify import slugify


def test_accents_removed_and_lowercased():
    assert slugify("Héllo Wörld!") == "hello-world"


def test_multiple_special_characters_collapse():
    assert slugify("foo***bar") == "foo-bar"
    assert slugify("foo   bar") == "foo-bar"


def test_leading_and_trailing_separators_stripped():
    assert slugify("  hello world  ") == "hello-world"
    assert slugify("!!!hello!!!") == "hello"


def test_umlauts():
    assert slugify("ÄÖÜ äöü") == "aou-aou"


def test_empty_input():
    assert slugify("") == ""


def test_underscore_is_preserved():
    assert slugify("hello_world") == "hello_world"


def test_length_limit():
    with pytest.raises(ValueError):
        slugify("a" * 1001)


def test_length_limit_boundary_ok():
    assert slugify("a" * 1000) == "a" * 1000


def test_type_error():
    with pytest.raises(TypeError):
        slugify(123)


def test_type_error_none():
    with pytest.raises(TypeError):
        slugify(None)


def test_error_message_hides_input():
    secret = "secret-token-xyz" * 100
    with pytest.raises(ValueError) as excinfo:
        slugify(secret)
    assert "secret-token-xyz" not in str(excinfo.value)
