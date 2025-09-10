"""Generate random floating-point numbers within a specified range."""

import random


def random_floats(count: int, min_value: float = 0.0, max_value: float = 1.0) -> list[float]:
    """
    Generate a list of random floating-point numbers within a specified range.

    Parameters
    ----------
    count : int
        Number of random floats to generate.
    min_value : float, optional
        Minimum value (inclusive). Defaults to 0.0.
    max_value : float, optional
        Maximum value (exclusive). Defaults to 1.0.

    Returns
    -------
    list[float]
        List of random floating-point numbers.

    Raises
    ------
    TypeError
        If count is not an integer or min_value/max_value are not numeric.
    ValueError
        If count is negative or min_value is greater than or equal to max_value.

    Examples
    --------
    >>> len(random_floats(5))
    5
    >>> all(0.0 <= x < 1.0 for x in random_floats(10))
    True
    >>> all(5.0 <= x < 10.0 for x in random_floats(5, 5.0, 10.0))
    True
    """
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    
    if not isinstance(min_value, (int, float)):
        raise TypeError("min_value must be numeric (int or float)")
    
    if not isinstance(max_value, (int, float)):
        raise TypeError("max_value must be numeric (int or float)")
    
    if count < 0:
        raise ValueError("count must be non-negative")
    
    if min_value >= max_value:
        raise ValueError("min_value must be less than max_value")
    
    return [random.uniform(min_value, max_value) for _ in range(count)]


__all__ = ['random_floats']
