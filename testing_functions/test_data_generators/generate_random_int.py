"""
Generate random integer for testing.
"""

import random


def generate_random_int(
    min_value: int = 0,
    max_value: int = 100,
) -> int:
    """
    Generate a random integer within specified range.

    Parameters
    ----------
    min_value : int, optional
        Minimum value (inclusive) (by default 0).
    max_value : int, optional
        Maximum value (inclusive) (by default 100).

    Returns
    -------
    int
        Random integer between min_value and max_value.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If min_value > max_value.

    Examples
    --------
    >>> result = generate_random_int(1, 10)
    >>> 1 <= result <= 10
    True
    >>> result = generate_random_int(0, 0)
    >>> result
    0

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(min_value, int):
        raise TypeError(f"min_value must be an integer, got {type(min_value).__name__}")
    if not isinstance(max_value, int):
        raise TypeError(f"max_value must be an integer, got {type(max_value).__name__}")
    
    if min_value > max_value:
        raise ValueError(f"min_value ({min_value}) must be <= max_value ({max_value})")
    
    return random.randint(min_value, max_value)


__all__ = ['generate_random_int']
