"""Calculate various types of medians and middle values for a list of numbers."""

from typing import Union
import math


def median(values: list[Union[int, float]], method: str = 'standard') -> float:
    """
    Calculate different types of medians and middle values for a list of numbers.

    Supports standard median, weighted median, geometric median approximation, and robust medians.

    Parameters
    ----------
    values : list[int | float]
        List of numeric values.
    method : str, optional
        Type of median to calculate. Options:
        - 'standard': Standard median (default)
        - 'low': Lower median (for even length, returns lower middle value)
        - 'high': Higher median (for even length, returns higher middle value)
        - 'midpoint': Same as standard (average of middle values for even length)
        - 'interpolated': Linear interpolation method
        - 'geometric': Geometric median approximation (1D case)

    Returns
    -------
    float
        The calculated median of the specified type.

    Raises
    ------
    TypeError
        If values is not a list or contains non-numeric values.
    ValueError
        If the list is empty or method is invalid.

    Examples
    --------
    >>> median([1, 2, 3, 4, 5])
    3.0
    >>> median([1, 2, 3, 4], method='low')
    2.0
    >>> median([1, 2, 3, 4], method='high')
    3.0
    """
    # Input validation
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    if not all(isinstance(value, (int, float)) for value in values):
        raise TypeError("all values must be numeric (int or float)")
    
    # Method validation
    valid_methods = ['standard', 'low', 'high', 'midpoint', 'interpolated', 'geometric']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    method = method.lower()
    
    # Calculate median based on method
    if method in ['standard', 'midpoint']:
        return _standard_median(values)
    elif method == 'low':
        return _low_median(values)
    elif method == 'high':
        return _high_median(values)
    elif method == 'interpolated':
        return _interpolated_median(values)
    elif method == 'geometric':
        return _geometric_median_1d(values)


def _standard_median(values: list[Union[int, float]]) -> float:
    """Calculate standard median."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 1:
        # Odd number of values
        return float(sorted_values[n // 2])
    else:
        # Even number of values - average of two middle values
        mid1 = sorted_values[n // 2 - 1]
        mid2 = sorted_values[n // 2]
        return (mid1 + mid2) / 2.0


def _low_median(values: list[Union[int, float]]) -> float:
    """Calculate low median (returns lower middle value for even length)."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 1:
        # Odd number of values
        return float(sorted_values[n // 2])
    else:
        # Even number of values - return lower middle value
        return float(sorted_values[n // 2 - 1])


def _high_median(values: list[Union[int, float]]) -> float:
    """Calculate high median (returns higher middle value for even length)."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n % 2 == 1:
        # Odd number of values
        return float(sorted_values[n // 2])
    else:
        # Even number of values - return higher middle value
        return float(sorted_values[n // 2])


def _interpolated_median(values: list[Union[int, float]], percentile: float = 50.0) -> float:
    """Calculate interpolated median using percentile method."""
    if not 0 <= percentile <= 100:
        raise ValueError("percentile must be between 0 and 100")
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    if n == 1:
        return float(sorted_values[0])
    
    # Calculate position using linear interpolation method
    position = (percentile / 100.0) * (n - 1)
    
    if position == int(position):
        # Exact index
        return float(sorted_values[int(position)])
    else:
        # Interpolate between two values
        lower_idx = int(position)
        upper_idx = lower_idx + 1
        weight = position - lower_idx
        
        if upper_idx >= n:
            return float(sorted_values[n - 1])
        
        lower_val = sorted_values[lower_idx]
        upper_val = sorted_values[upper_idx]
        
        return lower_val + weight * (upper_val - lower_val)


def _geometric_median_1d(values: list[Union[int, float]], max_iterations: int = 100, tolerance: float = 1e-8) -> float:
    """
    Calculate geometric median for 1D data using iterative method.
    
    The geometric median minimizes the sum of absolute deviations.
    For 1D data, this is equivalent to the standard median, but this
    implementation uses the general geometric median algorithm.
    """
    if len(values) == 1:
        return float(values[0])
    
    # Initial guess - use standard median
    x = _standard_median(values)
    
    for iteration in range(max_iterations):
        # Calculate weighted average
        numerator = 0.0
        denominator = 0.0
        
        for val in values:
            distance = abs(val - x)
            if distance > tolerance:  # Avoid division by zero
                weight = 1.0 / distance
                numerator += weight * val
                denominator += weight
            else:
                # Point is very close to current estimate
                return val
        
        if denominator == 0:
            break
        
        new_x = numerator / denominator
        
        # Check convergence
        if abs(new_x - x) < tolerance:
            return new_x
        
        x = new_x
    
    return x


def weighted_median(values: list[Union[int, float]], weights: list[Union[int, float]]) -> float:
    """
    Calculate weighted median.
    
    Parameters
    ----------
    values : list[int | float]
        List of numeric values.
    weights : list[int | float]
        List of weights corresponding to values.
    
    Returns
    -------
    float
        The weighted median.
    
    Raises
    ------
    ValueError
        If values and weights have different lengths or weights are invalid.
    """
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    
    if not all(w >= 0 for w in weights):
        raise ValueError("all weights must be non-negative")
    
    if sum(weights) == 0:
        raise ValueError("sum of weights must be positive")
    
    # Create sorted pairs of (value, weight)
    paired = list(zip(values, weights))
    paired.sort(key=lambda x: x[0])
    
    # Find weighted median
    total_weight = sum(weights)
    cumulative_weight = 0.0
    
    for value, weight in paired:
        cumulative_weight += weight
        
        if cumulative_weight >= total_weight / 2:
            return float(value)
    
    # Should not reach here with valid inputs
    return float(paired[-1][0])


__all__ = ['median']
