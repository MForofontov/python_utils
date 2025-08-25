"""
Advanced interpolation methods for numerical data.

This module provides various interpolation techniques including linear,
polynomial, spline, and other advanced interpolation methods.
"""

import math
from typing import List, Union, Dict, Any, Tuple, Optional


def interpolation(x_points: List[Union[int, float]], 
                 y_points: List[Union[int, float]], 
                 x_new: Union[float, List[float]], 
                 method: str = 'linear',
                 **kwargs) -> Union[float, List[float]]:
    """
    Perform interpolation using various methods.

    Interpolates data points to estimate values at new x positions using
    different interpolation techniques.

    Parameters
    ----------
    x_points : list of int or float
        X-coordinates of data points. Must be sorted in ascending order.
    y_points : list of int or float
        Y-coordinates of data points. Must have same length as x_points.
    x_new : float or list of float
        X-coordinate(s) where to interpolate values.
    method : str, optional
        Interpolation method to use. Options:
        - 'linear': Linear interpolation between adjacent points (default)
        - 'polynomial': Polynomial interpolation using all points
        - 'lagrange': Lagrange polynomial interpolation
        - 'newton': Newton polynomial interpolation
        - 'cubic_spline': Cubic spline interpolation (simplified)
        - 'nearest': Nearest neighbor interpolation
    **kwargs : dict
        Additional parameters for specific methods:
        - degree : int, polynomial degree for polynomial methods (default: len(x_points)-1)
        - extrapolate : bool, whether to extrapolate outside data range (default: False)

    Returns
    -------
    float or list of float
        Interpolated value(s) at x_new position(s).

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If data validation fails or method is unknown.

    Examples
    --------
    >>> x = [1, 2, 3, 4, 5]
    >>> y = [2, 4, 6, 8, 10]
    >>> interpolation(x, y, 2.5)
    5.0
    >>> interpolation(x, y, [1.5, 3.5], method='linear')
    [3.0, 7.0]

    Notes
    -----
    Linear interpolation is fastest and most stable for monotonic data.
    Polynomial interpolation may suffer from Runge's phenomenon for high degrees.
    """
    # Input validation
    if not isinstance(x_points, list) or not isinstance(y_points, list):
        raise TypeError("x_points and y_points must be lists")
    
    if len(x_points) != len(y_points):
        raise ValueError("x_points and y_points must have the same length")
    
    if len(x_points) < 2:
        raise ValueError("need at least 2 data points for interpolation")
    
    # Validate numeric types
    for i, (x, y) in enumerate(zip(x_points, y_points)):
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError(f"x_points must contain numeric values, found {type(x).__name__} at index {i}")
        if not isinstance(y, (int, float)) or isinstance(y, bool):
            raise TypeError(f"y_points must contain numeric values, found {type(y).__name__} at index {i}")
    
    # Check if x_points are sorted
    if not all(x_points[i] <= x_points[i+1] for i in range(len(x_points)-1)):
        raise ValueError("x_points must be sorted in ascending order")
    
    # Validate method
    valid_methods = ['linear', 'polynomial', 'lagrange', 'newton', 'cubic_spline', 'nearest']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    # Handle single value vs list input
    single_value = not isinstance(x_new, list)
    if single_value:
        x_new = [x_new]
    
    # Validate x_new values
    for i, x in enumerate(x_new):
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError(f"x_new must contain numeric values, found {type(x).__name__} at index {i}")
    
    # Get parameters
    extrapolate = kwargs.get('extrapolate', False)
    degree = kwargs.get('degree', len(x_points) - 1)
    
    # Check bounds unless extrapolating
    if not extrapolate:
        for x in x_new:
            if x < x_points[0] or x > x_points[-1]:
                raise ValueError(f"x_new value {x} is outside data range [{x_points[0]}, {x_points[-1]}]. Set extrapolate=True to allow.")
    
    method = method.lower()
    
    # Perform interpolation
    if method == 'linear':
        results = [_linear_interpolation(x_points, y_points, x) for x in x_new]
    elif method == 'polynomial':
        results = [_polynomial_interpolation(x_points, y_points, x, degree) for x in x_new]
    elif method == 'lagrange':
        results = [_lagrange_interpolation(x_points, y_points, x) for x in x_new]
    elif method == 'newton':
        results = [_newton_interpolation(x_points, y_points, x) for x in x_new]
    elif method == 'cubic_spline':
        results = [_cubic_spline_interpolation(x_points, y_points, x) for x in x_new]
    elif method == 'nearest':
        results = [_nearest_neighbor_interpolation(x_points, y_points, x) for x in x_new]
    
    return results[0] if single_value else results


def _linear_interpolation(x_points: List[float], y_points: List[float], x: float) -> float:
    """Perform linear interpolation."""
    n = len(x_points)
    
    # Handle edge cases
    if x <= x_points[0]:
        return y_points[0]
    if x >= x_points[-1]:
        return y_points[-1]
    
    # Find the interval containing x
    for i in range(n - 1):
        if x_points[i] <= x <= x_points[i + 1]:
            # Linear interpolation formula
            x0, x1 = x_points[i], x_points[i + 1]
            y0, y1 = y_points[i], y_points[i + 1]
            
            if x1 == x0:  # Avoid division by zero
                return y0
            
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    
    return y_points[-1]  # Fallback


def _polynomial_interpolation(x_points: List[float], y_points: List[float], x: float, degree: int) -> float:
    """Perform polynomial interpolation using Newton's method."""
    n = len(x_points)
    degree = min(degree, n - 1)
    
    # Use subset of points if degree is less than n-1
    if degree < n - 1:
        # Find closest points to x
        distances = [(abs(x - x_points[i]), i) for i in range(n)]
        distances.sort()
        indices = [distances[i][1] for i in range(degree + 1)]
        indices.sort()
        
        x_subset = [x_points[i] for i in indices]
        y_subset = [y_points[i] for i in indices]
    else:
        x_subset, y_subset = x_points, y_points
    
    return _newton_interpolation(x_subset, y_subset, x)


def _lagrange_interpolation(x_points: List[float], y_points: List[float], x: float) -> float:
    """Perform Lagrange polynomial interpolation."""
    n = len(x_points)
    result = 0.0
    
    for i in range(n):
        # Calculate Lagrange basis polynomial L_i(x)
        basis = 1.0
        for j in range(n):
            if i != j:
                if x_points[i] == x_points[j]:
                    raise ValueError("x_points must contain unique values for Lagrange interpolation")
                basis *= (x - x_points[j]) / (x_points[i] - x_points[j])
        
        result += y_points[i] * basis
    
    return result


def _newton_interpolation(x_points: List[float], y_points: List[float], x: float) -> float:
    """Perform Newton polynomial interpolation."""
    n = len(x_points)
    
    # Calculate divided differences table
    divided_diff = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # Initialize first column with y values
    for i in range(n):
        divided_diff[i][0] = y_points[i]
    
    # Calculate divided differences
    for j in range(1, n):
        for i in range(n - j):
            if x_points[i + j] == x_points[i]:
                raise ValueError("x_points must contain unique values for Newton interpolation")
            divided_diff[i][j] = (divided_diff[i + 1][j - 1] - divided_diff[i][j - 1]) / (x_points[i + j] - x_points[i])
    
    # Evaluate Newton polynomial at x
    result = divided_diff[0][0]
    product = 1.0
    
    for i in range(1, n):
        product *= (x - x_points[i - 1])
        result += divided_diff[0][i] * product
    
    return result


def _cubic_spline_interpolation(x_points: List[float], y_points: List[float], x: float) -> float:
    """Perform simplified cubic spline interpolation."""
    # This is a simplified version - real cubic splines require solving tridiagonal system
    # For now, use piecewise cubic interpolation with natural boundary conditions
    
    n = len(x_points)
    if n < 4:
        # Fall back to polynomial interpolation for small datasets
        return _newton_interpolation(x_points, y_points, x)
    
    # Find the interval containing x
    for i in range(n - 1):
        if x_points[i] <= x <= x_points[i + 1]:
            # Use local cubic interpolation with neighboring points
            start_idx = max(0, i - 1)
            end_idx = min(n, i + 3)
            
            x_local = x_points[start_idx:end_idx]
            y_local = y_points[start_idx:end_idx]
            
            return _newton_interpolation(x_local, y_local, x)
    
    # Outside range - use linear extrapolation
    return _linear_interpolation(x_points, y_points, x)


def _nearest_neighbor_interpolation(x_points: List[float], y_points: List[float], x: float) -> float:
    """Perform nearest neighbor interpolation."""
    n = len(x_points)
    
    # Find the closest point
    min_distance = float('inf')
    closest_idx = 0
    
    for i in range(n):
        distance = abs(x - x_points[i])
        if distance < min_distance:
            min_distance = distance
            closest_idx = i
    
    return y_points[closest_idx]


__all__ = ['interpolation']
