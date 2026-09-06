"""Tests für validkit.isbn.is_valid_isbn13."""

import pytest

from validkit.isbn import is_valid_isbn13


def test_valid_isbn_with_separators():
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_valid_isbn_plain_digits():
    assert is_valid_isbn13("9783161484100") is True


def test_valid_isbn_with_spaces():
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_wrong_check_digit_returns_false():
    assert is_valid_isbn13("978-3-16-148410-1") is False


def test_wrong_check_digit_plain_returns_false():
    assert is_valid_isbn13("9783161484101") is False


@pytest.mark.parametrize(
    "bad",
    [
        "97831614841",  # 11 Ziffern
        "97831614841000",  # 14 Ziffern
        "97831614841X",  # nicht-ziffernartig
        "abc-def-ghi",  # keine Ziffern
        "",  # leer
    ],
)
def test_invalid_input_raises_value_error(bad):
    with pytest.raises(ValueError):
        is_valid_isbn13(bad)


def test_length_limit_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("1" * 1001)


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(9783161484100)  # int


def test_non_string_none_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(None)


def test_error_message_does_not_leak_input():
    bad = "97831614841X"
    with pytest.raises(ValueError) as excinfo:
        is_valid_isbn13(bad)
    assert bad not in str(excinfo.value)
