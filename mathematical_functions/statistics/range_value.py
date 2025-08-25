"""Calculate the range of a list of numbers."""

from typing import Union


def range_value(values: list[Union[int, float]]) -> Union[int, float]:
    """
    Calculate the range (difference between max and min) of a list of numbers.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.

    Returns
    -------
    int | float
        The range of the input values (max - min). Returns the same type as
        the difference between max and min values.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values.
    ValueError
        If the list is empty.

    Examples
    --------
    >>> range_value([1, 2, 3, 4, 5])
    4
    >>> range_value([10.5, 2.3, 8.7])
    8.2
    >>> range_value([5, 5, 5])
    0
    >>> range_value([-3, 7, 2])
    10
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    return max(values) - min(values)


__all__ = ['range_value']
