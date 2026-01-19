"""
Generate random float for testing.
"""

import random


def generate_random_float(
    min_value: float = 0.0,
    max_value: float = 1.0,
    precision: int = 2,
) -> float:
    """
    Generate a random float within specified range.

    Parameters
    ----------
    min_value : float, optional
        Minimum value (by default 0.0).
    max_value : float, optional
        Maximum value (by default 1.0).
    precision : int, optional
        Number of decimal places (by default 2).

    Returns
    -------
    float
        Random float between min_value and max_value.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If min_value > max_value or precision is negative.

    Examples
    --------
    >>> result = generate_random_float(0.0, 1.0, 2)
    >>> 0.0 <= result <= 1.0
    True
    >>> result = generate_random_float(5.0, 10.0, 1)
    >>> 5.0 <= result <= 10.0
    True

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(min_value, (int, float)):
        raise TypeError(f"min_value must be a number, got {type(min_value).__name__}")
    if not isinstance(max_value, (int, float)):
        raise TypeError(f"max_value must be a number, got {type(max_value).__name__}")
    if not isinstance(precision, int):
        raise TypeError(f"precision must be an integer, got {type(precision).__name__}")

    if min_value > max_value:
        raise ValueError(f"min_value ({min_value}) must be <= max_value ({max_value})")
    if precision < 0:
        raise ValueError(f"precision must be non-negative, got {precision}")

    value = random.uniform(min_value, max_value)
    return round(value, precision)


__all__ = ["generate_random_float"]
