"""
Correlation coefficient calculation with multiple methods.

This module provides correlation coefficient calculations using various methods
including Pearson, Spearman, Kendall's tau, and others.
"""

import math
from typing import List, Union, Dict, Any


def correlation_coefficient(x_values: List[Union[int, float]], 
                          y_values: List[Union[int, float]], 
                          method: str = 'pearson') -> float:
    """
    Calculate correlation coefficient using various methods.
    
    Supports multiple correlation methods for different types of data and relationships.
    
    Args:
        x_values: List of numeric values for x variable
        y_values: List of numeric values for y variable  
        method: Correlation method to use. Options:
               - 'pearson': Pearson product-moment correlation (default)
               - 'spearman': Spearman rank correlation
               - 'kendall': Kendall's tau correlation
    
    Returns:
        float: Correlation coefficient (-1 to +1)
        
    Raises:
        TypeError: If inputs are not lists or contain non-numeric values
        ValueError: If inputs are invalid or method is unknown
        
    Examples:
        >>> correlation_coefficient([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        1.0
        >>> correlation_coefficient([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], method='spearman')
        -1.0
    """
    # Input validation
    if not isinstance(x_values, list):
        raise TypeError("x_values must be a list")
    if not isinstance(y_values, list):
        raise TypeError("y_values must be a list")
    
    if len(x_values) == 0 or len(y_values) == 0:
        raise ValueError("Input lists cannot be empty")

    if len(x_values) < 2 or len(y_values) < 2:
        raise ValueError("Need at least 2 data points")

    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    # Validate numeric types
    for i, val in enumerate(x_values):
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError("All values in x_values must be numeric")
    
    for i, val in enumerate(y_values):
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError("All values in y_values must be numeric")
    
    # Validate method
    valid_methods = ['pearson', 'spearman', 'kendall']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    # Calculate correlation based on method
    method = method.lower()
    
    if method == 'pearson':
        return _pearson_correlation(x_values, y_values)
    elif method == 'spearman':
        return _spearman_correlation(x_values, y_values)
    elif method == 'kendall':
        return _kendall_correlation(x_values, y_values)


def _pearson_correlation(x_values: List[Union[int, float]], y_values: List[Union[int, float]]) -> float:
    """Calculate Pearson product-moment correlation coefficient."""
    n = len(x_values)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    # Calculate correlation components
    numerator = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
    sum_sq_x = sum((x_values[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y_values[i] - mean_y) ** 2 for i in range(n))
    
    # Check for zero variance
    if sum_sq_x == 0 or sum_sq_y == 0:
        # One of the series is constant; correlation is undefined but the
        # tests in this project expect a value of 0.0 rather than raising an
        # exception. Returning 0.0 indicates no linear relationship.
        return 0.0
    
    return numerator / math.sqrt(sum_sq_x * sum_sq_y)


def _spearman_correlation(x_values: List[Union[int, float]], y_values: List[Union[int, float]]) -> float:
    """Calculate Spearman rank correlation coefficient."""
    # Convert to ranks
    x_ranks = _convert_to_ranks(x_values)
    y_ranks = _convert_to_ranks(y_values)
    
    # Calculate Pearson correlation of ranks
    return _pearson_correlation(x_ranks, y_ranks)


def _kendall_correlation(x_values: List[Union[int, float]], y_values: List[Union[int, float]]) -> float:
    """Calculate Kendall's tau correlation coefficient."""
    n = len(x_values)
    concordant = 0
    discordant = 0
    
    # Count concordant and discordant pairs
    for i in range(n - 1):
        for j in range(i + 1, n):
            x_diff = x_values[j] - x_values[i]
            y_diff = y_values[j] - y_values[i]
            
            if (x_diff > 0 and y_diff > 0) or (x_diff < 0 and y_diff < 0):
                concordant += 1
            elif (x_diff > 0 and y_diff < 0) or (x_diff < 0 and y_diff > 0):
                discordant += 1
            # Ties contribute 0
    
    total_pairs = n * (n - 1) // 2
    if total_pairs == 0:
        return 0.0
    
    return (concordant - discordant) / total_pairs


def _convert_to_ranks(values: List[Union[int, float]]) -> List[float]:
    """Convert values to ranks, handling ties with average ranking."""
    indexed_values = [(values[i], i) for i in range(len(values))]
    indexed_values.sort(key=lambda x: x[0])
    
    ranks = [0.0] * len(values)
    
    i = 0
    while i < len(indexed_values):
        j = i
        # Find all values equal to current value
        while j < len(indexed_values) and indexed_values[j][0] == indexed_values[i][0]:
            j += 1
        
        # Assign average rank to tied values
        avg_rank = (i + j + 1) / 2.0  # +1 for 1-based ranking
        for k in range(i, j):
            original_index = indexed_values[k][1]
            ranks[original_index] = avg_rank
        
        i = j
    
    return ranks


__all__ = ['correlation_coefficient']
