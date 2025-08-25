"""Calculate the arithmetic mean of a list of numbers."""

from typing import Union


def mean(values: list[Union[int, float]]) -> float:
    """
    Calculate the arithmetic mean (average) of a list of numbers.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.

    Returns
    -------
    float
        The arithmetic mean of the input values.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values.
    ValueError
        If the list is empty.

    Examples
    --------
    >>> mean([1, 2, 3, 4, 5])
    3.0
    >>> mean([10, 20, 30])
    20.0
    >>> mean([1.5, 2.5, 3.5])
    2.5
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    return sum(values) / len(values)


__all__ = ['mean']
