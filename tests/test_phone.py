"""Tests für validkit.phone.normalize_phone."""

import pytest

from validkit.phone import normalize_phone


def test_normalize_parentheses_spaces_hyphens():
    assert normalize_phone("(030) 1234-567", "DE") == "+49301234567"


def test_normalize_dots():
    assert normalize_phone("030.1234.567", "DE") == "+49301234567"


def test_normalize_leading_zero_removed():
    assert normalize_phone("030123456", "DE") == "+4930123456"


def test_normalize_inner_spaces():
    assert normalize_phone("0 1 234 567", "AT") == "+431234567"


def test_normalize_us_with_parentheses():
    assert normalize_phone("(555) 123-4567", "US") == "+15551234567"


@pytest.mark.parametrize(
    "country_code,expected",
    [
        ("DE", "49"),
        ("AT", "43"),
        ("CH", "41"),
        ("US", "1"),
        ("GB", "44"),
        ("FR", "33"),
        ("NL", "31"),
        ("IT", "39"),
        ("ES", "34"),
    ],
)
def test_country_code_mapping(country_code, expected):
    assert normalize_phone("030123456", country_code) == "+" + expected + "30123456"


def test_unknown_country_code_raises():
    with pytest.raises(ValueError):
        normalize_phone("030123456", "XX")


def test_lowercase_country_code_raises():
    with pytest.raises(ValueError):
        normalize_phone("030123456", "de")


def test_too_few_digits_raises():
    with pytest.raises(ValueError):
        normalize_phone("123", "DE")


def test_no_digits_raises():
    with pytest.raises(ValueError):
        normalize_phone("(  )", "DE")


def test_letters_are_not_formatting_raise():
    with pytest.raises(ValueError):
        normalize_phone("abc123456", "DE")


def test_mixed_alphanumeric_raises():
    with pytest.raises(ValueError):
        normalize_phone("(030) 12x4-567", "DE")


def test_only_five_digits_raises():
    with pytest.raises(ValueError):
        normalize_phone("12345", "DE")


def test_six_digits_ok():
    assert normalize_phone("123456", "DE") == "+49123456"


def test_length_limit_raises():
    with pytest.raises(ValueError):
        normalize_phone("1" * 1001, "DE")


def test_length_limit_exactly_1000_allowed():
    assert normalize_phone("1" * 1000, "DE") == "+49" + "1" * 1000


def test_non_string_text_raises_type_error():
    with pytest.raises(TypeError):
        normalize_phone(123456, "DE")


def test_non_string_country_code_raises_type_error():
    with pytest.raises(TypeError):
        normalize_phone("030123456", 49)


def test_error_message_does_not_contain_number():
    with pytest.raises(ValueError) as exc_info:
        normalize_phone("030 1234-567", "XX")
    assert "030" not in str(exc_info.value)
    assert "1234567" not in str(exc_info.value)
