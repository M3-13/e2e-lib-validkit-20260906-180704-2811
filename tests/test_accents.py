"""Tests für validkit.accents.strip_accents."""

import pytest

from validkit.accents import strip_accents


def test_strip_accents_basic():
    assert strip_accents("café") == "cafe"


def test_strip_accents_multiple_words():
    assert strip_accents("crème brûlée") == "creme brulee"


def test_strip_accents_plain_text_unchanged():
    assert strip_accents("cafe") == "cafe"
    assert strip_accents("hello world") == "hello world"


def test_strip_accents_german_umlauts():
    assert strip_accents("Über") == "Uber"


def test_strip_accents_combining_sequences():
    assert strip_accents("e\u0301") == "e"
    assert strip_accents("u\u0308") == "u"


def test_strip_accents_empty_string():
    assert strip_accents("") == ""


def test_strip_accents_length_limit():
    assert strip_accents("a" * 1000) == "a" * 1000
    with pytest.raises(ValueError):
        strip_accents("a" * 1001)


def test_strip_accents_type_error():
    with pytest.raises(TypeError):
        strip_accents(123)
    with pytest.raises(TypeError):
        strip_accents(None)


def test_strip_accents_error_message_hides_input():
    with pytest.raises(ValueError) as excinfo:
        strip_accents("é" * 1001)
    assert "é" not in str(excinfo.value)
