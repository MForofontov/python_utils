"""Calculate the skewness of a list of numbers."""

from typing import Union
import math


def skewness(values: list[Union[int, float]]) -> float:
    """
    Calculate the skewness of a list of numbers.

    Skewness measures the asymmetry of the distribution. Positive skewness 
    indicates a distribution with a tail extending to the right, negative 
    skewness indicates a tail extending to the left.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values (must have at least 3 elements).

    Returns
    -------
    float
        The skewness of the input values.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values.
    ValueError
        If the list has fewer than 3 elements or all values are identical.

    Examples
    --------
    >>> abs(skewness([1, 2, 3, 4, 5]) - 0.0) < 1e-10  # symmetric
    True
    >>> skewness([1, 1, 1, 2, 3, 4, 5]) > 0  # positive skew
    True
    >>> skewness([1, 2, 3, 4, 5, 5, 5]) < 0  # negative skew
    True
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) < 3:
        raise ValueError("skewness requires at least 3 values")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    # Calculate mean
    mean_val = sum(values) / len(values)
    
    # Calculate standard deviation
    squared_diffs = [(x - mean_val) ** 2 for x in values]
    variance_val = sum(squared_diffs) / (len(values) - 1)
    
    if variance_val == 0:
        raise ValueError("all values are identical, cannot calculate skewness")
    
    std_dev = math.sqrt(variance_val)
    
    # Calculate skewness
    cubed_diffs = [((x - mean_val) / std_dev) ** 3 for x in values]
    skewness_val = sum(cubed_diffs) / len(values)
    
    return skewness_val


__all__ = ['skewness']
