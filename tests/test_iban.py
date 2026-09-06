"""Tests für validkit.iban.is_valid_iban."""

import pytest

from validkit.iban import is_valid_iban


def test_valid_iban_with_spaces():
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_valid_iban_without_spaces():
    assert is_valid_iban("DE89370400440532013000") is True


def test_invalid_check_digit():
    assert is_valid_iban("DE88 3704 0044 0532 0130 00") is False


def test_too_short_raises_valueerror():
    with pytest.raises(ValueError):
        is_valid_iban("DE12")


def test_non_alphanumeric_raises_valueerror():
    with pytest.raises(ValueError):
        is_valid_iban("DE89 3704 0044 0532 0130 0!")


def test_length_limit_raises_valueerror():
    with pytest.raises(ValueError):
        is_valid_iban("A" * 1001)


def test_non_string_raises_typeerror():
    with pytest.raises(TypeError):
        is_valid_iban(1234567890)


def test_none_raises_typeerror():
    with pytest.raises(TypeError):
        is_valid_iban(None)


def test_error_message_does_not_contain_input():
    with pytest.raises(ValueError) as exc_info:
        is_valid_iban("DE12")
    assert "DE12" not in str(exc_info.value)
