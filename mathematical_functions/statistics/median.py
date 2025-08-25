"""Calculate the median of a list of numbers."""

from typing import Union


def median(values: list[Union[int, float]]) -> float:
    """
    Calculate the median (middle value) of a list of numbers.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.

    Returns
    -------
    float
        The median of the input values. For even-length lists, returns the 
        average of the two middle values.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values.
    ValueError
        If the list is empty.

    Examples
    --------
    >>> median([1, 2, 3, 4, 5])
    3.0
    >>> median([1, 2, 3, 4])
    2.5
    >>> median([5, 1, 3, 2, 4])
    3.0
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 1:
        # Odd number of values
        return float(sorted_values[n // 2])
    else:
        # Even number of values
        mid1 = sorted_values[n // 2 - 1]
        mid2 = sorted_values[n // 2]
        return (mid1 + mid2) / 2.0


__all__ = ['median']
