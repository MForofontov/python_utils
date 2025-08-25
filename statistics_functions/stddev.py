"""Calculate the standard deviation of a list of numbers."""

from typing import Union
import math


def stddev(values: list[Union[int, float]], sample: bool = True) -> float:
    """
    Calculate the standard deviation of a list of numbers.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.
    sample : bool, optional
        If True (default), calculates sample standard deviation (divides by n-1).
        If False, calculates population standard deviation (divides by n).

    Returns
    -------
    float
        The standard deviation of the input values.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values, or if sample 
        is not a boolean.
    ValueError
        If the list is empty or has only one element when sample=True.

    Examples
    --------
    >>> stddev([1, 2, 3, 4, 5])
    1.5811388300841898
    >>> stddev([1, 2, 3, 4, 5], sample=False)
    1.4142135623730951
    >>> stddev([10, 10, 10, 10])
    0.0
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if not isinstance(sample, bool):
        raise TypeError("sample must be a boolean")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if sample and len(values) == 1:
        raise ValueError("sample standard deviation requires at least 2 values")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    # Calculate mean
    mean_value = sum(values) / len(values)
    
    # Calculate sum of squared differences
    squared_diffs = [(x - mean_value) ** 2 for x in values]
    variance = sum(squared_diffs) / (len(values) - 1 if sample else len(values))
    
    return math.sqrt(variance)


__all__ = ['stddev']
