"""Generate random integers within a specified range."""

import random


def random_integers(count: int, min_value: int = 0, max_value: int = 100) -> list[int]:
    """
    Generate a list of random integers within a specified range.

    Parameters
    ----------
    count : int
        Number of random integers to generate.
    min_value : int, optional
        Minimum value (inclusive). Defaults to 0.
    max_value : int, optional
        Maximum value (inclusive). Defaults to 100.

    Returns
    -------
    list[int]
        List of random integers.

    Raises
    ------
    TypeError
        If count, min_value, or max_value is not an integer.
    ValueError
        If count is negative or min_value is greater than max_value.

    Examples
    --------
    >>> len(random_integers(5))
    5
    >>> all(0 <= x <= 100 for x in random_integers(10))
    True
    >>> all(10 <= x <= 20 for x in random_integers(5, 10, 20))
    True
    """
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    
    if not isinstance(min_value, int):
        raise TypeError("min_value must be an integer")
    
    if not isinstance(max_value, int):
        raise TypeError("max_value must be an integer")
    
    if count < 0:
        raise ValueError("count must be non-negative")
    
    if min_value > max_value:
        raise ValueError("min_value must be less than or equal to max_value")
    
    return [random.randint(min_value, max_value) for _ in range(count)]


__all__ = ['random_integers']
