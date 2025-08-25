"""Generate normally distributed random numbers."""

import random
from typing import Union


def random_normal(count: int, mean: float = 0.0, stddev: float = 1.0) -> list[float]:
    """
    Generate a list of normally distributed random numbers.

    Parameters
    ----------
    count : int
        Number of random numbers to generate.
    mean : float, optional
        Mean of the normal distribution. Defaults to 0.0.
    stddev : float, optional
        Standard deviation of the normal distribution. Defaults to 1.0.

    Returns
    -------
    list[float]
        List of normally distributed random numbers.

    Raises
    ------
    TypeError
        If count is not an integer or mean/stddev are not numeric.
    ValueError
        If count is negative or stddev is non-positive.

    Examples
    --------
    >>> len(random_normal(100))
    100
    >>> data = random_normal(1000, mean=10.0, stddev=2.0)
    >>> abs(sum(data) / len(data) - 10.0) < 1.0  # Mean should be close to 10
    True
    """
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    
    if not isinstance(mean, (int, float)):
        raise TypeError("mean must be numeric (int or float)")
    
    if not isinstance(stddev, (int, float)):
        raise TypeError("stddev must be numeric (int or float)")
    
    if count < 0:
        raise ValueError("count must be non-negative")
    
    if stddev <= 0:
        raise ValueError("stddev must be positive")
    
    return [random.normalvariate(mean, stddev) for _ in range(count)]


__all__ = ['random_normal']
