"""Tests für validkit.email.is_valid_email."""

import pytest

from validkit.email import is_valid_email


@pytest.mark.parametrize(
    "address",
    [
        "a@b.co",
        "a.b+c@example.com",
        "user.name+tag@sub.domain-example.co",
    ],
)
def test_valid_addresses(address):
    assert is_valid_email(address) is True


@pytest.mark.parametrize(
    "address",
    [
        "a@b",
        "a b@c.de",
        "a@",
        "@b.co",
        "a..b@c.de",
        ".a@b.co",
        "a.@b.co",
        "a@b.123",
        "a@b..co",
        "a@@b.co",
    ],
)
def test_invalid_addresses(address):
    assert is_valid_email(address) is False


def test_type_error_on_non_str():
    with pytest.raises(TypeError):
        is_valid_email(123)
    with pytest.raises(TypeError):
        is_valid_email(None)


def test_value_error_on_too_long():
    with pytest.raises(ValueError):
        is_valid_email("a" * 1001 + "@b.co")


def test_max_length_accepted():
    assert is_valid_email("a" * 993 + "@b.co") is True


def test_error_messages_do_not_leak_input():
    with pytest.raises(TypeError) as excinfo:
        is_valid_email(42)
    assert "42" not in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        is_valid_email("SENSIBLE" * 200)
    message = str(excinfo.value)
    assert "SENSIBLE" not in message
    assert "1000" in message
