"""Calculate quantiles of a list of numbers."""

from typing import Union


def quantile(values: list[Union[int, float]], q: float) -> float:
    """
    Calculate the q-th quantile of a list of numbers.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.
    q : float
        Quantile level (between 0 and 1, inclusive).

    Returns
    -------
    float
        The q-th quantile of the input values.

    Raises
    ------
    TypeError
        If values is not a list, contains non-numeric values, or q is not numeric.
    ValueError
        If the list is empty or q is not between 0 and 1.

    Examples
    --------
    >>> quantile([1, 2, 3, 4, 5], 0.5)  # median
    3.0
    >>> quantile([1, 2, 3, 4, 5], 0.25)  # first quartile
    2.0
    >>> quantile([1, 2, 3, 4, 5], 0.75)  # third quartile
    4.0
    >>> quantile([1, 2, 3, 4], 0.5)
    2.5
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if not isinstance(q, (int, float)):
        raise TypeError("q must be numeric (int or float)")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if not (0 <= q <= 1):
        raise ValueError("q must be between 0 and 1 (inclusive)")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if q == 0:
        return float(sorted_values[0])
    if q == 1:
        return float(sorted_values[-1])
    
    # Calculate position
    position = q * (n - 1)
    lower_index = int(position)
    upper_index = min(lower_index + 1, n - 1)
    weight = position - lower_index
    
    # Linear interpolation
    return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight


__all__ = ['quantile']
