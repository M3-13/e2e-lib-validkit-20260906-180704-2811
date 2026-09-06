"""Werte-Clamping."""

from numbers import Real


def clamp(value: float, low: float, high: float) -> float:
    """Begrenze *value* auf das Intervall [*low*, *high*]."""
    for name, arg in (("value", value), ("low", low), ("high", high)):
        if isinstance(arg, bool) or not isinstance(arg, Real):
            raise TypeError(f"{name} muss eine Zahl sein")
    if low > high:
        raise ValueError("low darf nicht größer als high sein")
    return min(max(value, low), high)
