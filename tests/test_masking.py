"""Tests für die Geheimnis-Maskierung."""

import pytest

from validkit import mask_secret


def test_mask_secret_keeps_last_four():
    assert mask_secret("geheim1234") == "******1234"


def test_mask_secret_keeps_only_last_keep_when_longer():
    assert mask_secret("abcdefgh", keep=2) == "******gh"


def test_mask_secret_shorter_than_keep_returns_only_stars():
    assert mask_secret("abc", keep=4) == "***"


def test_mask_secret_equal_to_keep_returns_only_stars():
    assert mask_secret("abcd", keep=4) == "****"


def test_mask_secret_keep_zero_masks_everything():
    assert mask_secret("abcd", keep=0) == "****"


def test_mask_secret_empty_text():
    assert mask_secret("") == ""


def test_mask_secret_negative_keep_raises():
    with pytest.raises(ValueError):
        mask_secret("geheim1234", keep=-1)


def test_mask_secret_non_str_text_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret(1234)


def test_mask_secret_non_int_keep_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret("geheim1234", keep="4")


def test_mask_secret_never_leaks_short_secret():
    for secret in ("a", "ab", "abc", "abcd"):
        assert mask_secret(secret, keep=4) == "*" * len(secret)


def test_mask_secret_error_message_does_not_contain_secret():
    secret = "topsecret1234"
    with pytest.raises(ValueError) as excinfo:
        mask_secret(secret, keep=-1)
    assert secret not in str(excinfo.value)
