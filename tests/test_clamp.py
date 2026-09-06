"""Tests für validkit.clamp."""

import pytest

from validkit import clamp


def test_clamp_within_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_range():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above_range():
    assert clamp(15, 0, 10) == 10


def test_clamp_lower_boundary():
    assert clamp(0, 0, 10) == 0


def test_clamp_upper_boundary():
    assert clamp(10, 0, 10) == 10


def test_clamp_floats():
    assert clamp(3.14, 0.0, 10.0) == 3.14
    assert clamp(-0.5, 0.0, 10.0) == 0.0
    assert clamp(12.5, 0.0, 10.0) == 10.0


def test_clamp_equal_bounds():
    assert clamp(5, 3, 3) == 3


def test_clamp_swapped_bounds_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


@pytest.mark.parametrize("args", [("x", 0, 10), (5, "x", 10), (5, 0, "x")])
def test_clamp_type_error(args):
    with pytest.raises(TypeError):
        clamp(*args)


def test_clamp_bool_rejected():
    with pytest.raises(TypeError):
        clamp(True, 0, 10)
