"""Calculate correlation coefficient between two datasets."""

from typing import Union
import math


def correlation(x: list[Union[int, float]], y: list[Union[int, float]], method: str = "pearson") -> float:
    """
    Calculate correlation coefficient between two datasets.

    Parameters
    ----------
    x : list[int | float]
        First dataset of numeric values.
    y : list[int | float] 
        Second dataset of numeric values (must be same length as x).
    method : str, optional
        Correlation method: "pearson" (default), "spearman".

    Returns
    -------
    float
        Correlation coefficient between -1 and 1.
        Values close to 1 indicate strong positive correlation,
        close to -1 indicate strong negative correlation,
        close to 0 indicate weak correlation.

    Raises
    ------
    TypeError
        If x or y is not a list, contains non-numeric values, or method is not string.
    ValueError
        If x and y have different lengths, have fewer than 2 elements,
        or method is not supported.

    Examples
    --------
    >>> correlation([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])  # perfect positive
    1.0
    >>> correlation([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])  # perfect negative
    -1.0
    >>> abs(correlation([1, 2, 3], [1, 2, 3]) - 1.0) < 1e-10
    True
    """
    # Input validation
    if not isinstance(x, list):
        raise TypeError("x must be a list")
    
    if not isinstance(y, list):
        raise TypeError("y must be a list")
    
    if not isinstance(method, str):
        raise TypeError("method must be a string")
    
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    if len(x) < 2:
        raise ValueError("datasets must have at least 2 elements")
    
    if not all(isinstance(val, (int, float)) for val in x):
        raise TypeError("all values in x must be numeric")
    
    if not all(isinstance(val, (int, float)) for val in y):
        raise TypeError("all values in y must be numeric")
    
    method = method.lower()
    if method not in ["pearson", "spearman"]:
        raise ValueError("method must be 'pearson' or 'spearman'")
    
    # Convert to ranks for Spearman correlation
    if method == "spearman":
        x = _rank_data(x)
        y = _rank_data(y)
    
    # Calculate means
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    # Calculate numerator and denominators
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
    
    sum_sq_x = sum((val - mean_x) ** 2 for val in x)
    sum_sq_y = sum((val - mean_y) ** 2 for val in y)
    
    # Handle zero variance cases
    if sum_sq_x == 0 or sum_sq_y == 0:
        if sum_sq_x == 0 and sum_sq_y == 0:
            return 1.0  # Both constant, perfectly correlated
        else:
            return 0.0  # One constant, no correlation
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    # Calculate correlation coefficient
    correlation_coeff = numerator / denominator
    
    # Clamp to [-1, 1] to handle floating point precision issues
    return max(-1.0, min(1.0, correlation_coeff))


def _rank_data(data: list[Union[int, float]]) -> list[float]:
    """
    Convert data to ranks, handling ties with average ranking.
    
    Parameters
    ----------
    data : list[int | float]
        Data to rank.
        
    Returns
    -------
    list[float]
        Ranks of the data.
    """
    # Create list of (value, original_index) pairs
    indexed_data = [(val, idx) for idx, val in enumerate(data)]
    
    # Sort by value
    indexed_data.sort(key=lambda x: x[0])
    
    # Assign ranks, handling ties
    ranks = [0.0] * len(data)
    i = 0
    
    while i < len(indexed_data):
        # Find all equal values
        j = i
        while j < len(indexed_data) and indexed_data[j][0] == indexed_data[i][0]:
            j += 1
        
        # Assign average rank to all equal values
        avg_rank = (i + j - 1) / 2 + 1  # +1 because ranks start at 1
        
        for k in range(i, j):
            original_idx = indexed_data[k][1]
            ranks[original_idx] = avg_rank
        
        i = j
    
    return ranks


__all__ = ['correlation']
