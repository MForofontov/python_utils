"""Calculate various types of means for a list of numbers."""

from typing import Union
import math


def mean(values: list[Union[int, float]], method: str = 'arithmetic') -> float:
    """
    Calculate different types of means for a list of numbers.

    Supports arithmetic, geometric, harmonic, quadratic (RMS), and trimmed means.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.
    method : str, optional
        Type of mean to calculate. Options:
        - 'arithmetic': Standard arithmetic mean (default)
        - 'geometric': Geometric mean (nth root of product)
        - 'harmonic': Harmonic mean (reciprocal of arithmetic mean of reciprocals)
        - 'quadratic': Quadratic mean (root mean square)
        - 'trimmed': Trimmed mean (excludes extreme values)

    Returns
    -------
    float
        The calculated mean of the specified type.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values.
    ValueError
        If the list is empty, method is invalid, or values are inappropriate for the method.

    Examples
    --------
    >>> mean([1, 2, 3, 4, 5])
    3.0
    >>> mean([1, 2, 4, 8], method='geometric')
    2.8284271247461903
    >>> mean([1, 2, 3, 4], method='harmonic')
    1.9200000000000004
    """
    # Input validation
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    # Method validation
    valid_methods = ['arithmetic', 'geometric', 'harmonic', 'quadratic', 'trimmed']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    method = method.lower()
    
    # Calculate mean based on method
    if method == 'arithmetic':
        return _arithmetic_mean(values)
    elif method == 'geometric':
        return _geometric_mean(values)
    elif method == 'harmonic':
        return _harmonic_mean(values)
    elif method == 'quadratic':
        return _quadratic_mean(values)
    elif method == 'trimmed':
        return _trimmed_mean(values)


def _arithmetic_mean(values: list[Union[int, float]]) -> float:
    """Calculate arithmetic mean."""
    return sum(values) / len(values)


def _geometric_mean(values: list[Union[int, float]]) -> float:
    """Calculate geometric mean."""
    # Check for non-positive values
    if any(val <= 0 for val in values):
        raise ValueError("geometric mean requires all positive values")
    
    # Use logarithms to avoid overflow
    log_sum = sum(math.log(val) for val in values)
    return math.exp(log_sum / len(values))


def _harmonic_mean(values: list[Union[int, float]]) -> float:
    """Calculate harmonic mean."""
    # Check for zero values
    if any(val == 0 for val in values):
        raise ValueError("harmonic mean is undefined when any value is zero")
    
    # Check for mixed signs
    signs = [1 if val > 0 else -1 for val in values]
    if len(set(signs)) > 1:
        raise ValueError("harmonic mean requires all values to have the same sign")
    
    reciprocal_sum = sum(1.0 / val for val in values)
    return len(values) / reciprocal_sum


def _quadratic_mean(values: list[Union[int, float]]) -> float:
    """Calculate quadratic mean (root mean square)."""
    sum_of_squares = sum(val ** 2 for val in values)
    return math.sqrt(sum_of_squares / len(values))


def _trimmed_mean(values: list[Union[int, float]], trim_percent: float = 0.2) -> float:
    """Calculate trimmed mean (excludes extreme values)."""
    if len(values) < 4:
        # Not enough values to trim meaningfully
        return _arithmetic_mean(values)
    
    # Sort values
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    # Calculate number of values to trim from each end
    trim_count = int(n * trim_percent / 2)
    
    if trim_count == 0:
        return _arithmetic_mean(values)
    
    # Trim extreme values
    trimmed_values = sorted_values[trim_count:-trim_count]
    
    if len(trimmed_values) == 0:
        return _arithmetic_mean(values)
    
    return sum(trimmed_values) / len(trimmed_values)


__all__ = ['mean']
