"""Tests für validkit.luhn.luhn_check."""

import pytest

from validkit.luhn import luhn_check


def test_valid_card_number():
    assert luhn_check("4532015112830366") is True


def test_reference_number():
    assert luhn_check("79927398713") is True


def test_transposed_digits_rejected():
    assert luhn_check("4532015112830636") is False


def test_single_digit_changed_rejected():
    assert luhn_check("4532015112830365") is False


def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("")


def test_non_digit_characters_raise_value_error():
    for value in ("12a4", "4532 015112830366", "4532-015112830366", "12.4", "\uff11\uff12\uff13"):
        with pytest.raises(ValueError):
            luhn_check(value)


def test_non_string_raises_type_error():
    for value in (4532015112830366, 79927398713, None, ["4532015112830366"]):
        with pytest.raises(TypeError):
            luhn_check(value)


def test_error_messages_do_not_contain_input():
    for value in ("12a4", "4532 015112830366"):
        with pytest.raises(ValueError) as exc_info:
            luhn_check(value)
        assert value not in str(exc_info.value)
    with pytest.raises(TypeError) as exc_info:
        luhn_check(4532015112830366)
    assert "4532015112830366" not in str(exc_info.value)
