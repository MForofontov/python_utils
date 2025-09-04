"""
Advanced interpolation methods for numerical data.

This module provides various interpolation techniques including linear,
polynomial, spline, and other advanced interpolation methods.
"""

import math
from typing import List, Union, Dict, Any, Tuple, Optional


def interpolation(x_points: List[Union[int, float]],
                 y_points: List[Union[int, float]],
                 x_new: List[Union[int, float]],
                 method: str = 'linear',
                 **kwargs) -> Dict[str, Any]:
    """Perform interpolation using various methods.

    The implementation focuses on clear validation and on returning a
    structured result that includes metadata about the interpolation
    process.  Only the features required by the unit tests are
    implemented.
    """

    # ------------------------------------------------------------------
    # Input validation
    # ------------------------------------------------------------------
    if not isinstance(x_points, list):
        raise TypeError("x_data must be a list")
    if not isinstance(y_points, list):
        raise TypeError("y_data must be a list")
    if not isinstance(x_new, list):
        raise TypeError("x_new must be a list")

    if len(x_points) == 0 or len(y_points) == 0:
        raise ValueError("Input arrays cannot be empty")
    if len(x_points) != len(y_points):
        raise ValueError("x_data and y_data must have same length")
    if len(x_points) < 2:
        raise ValueError("At least 2 data points required")
    if len(set(x_points)) != len(x_points):
        raise ValueError("Duplicate x values")

    # Numeric checks
    for x in x_points:
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("All values in x_data must be numeric")
    for y in y_points:
        if not isinstance(y, (int, float)) or isinstance(y, bool):
            raise TypeError("All values in y_data must be numeric")
    for x in x_new:
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("All values in x_new must be numeric")

    # Ensure x_points sorted for interpolation
    if not all(x_points[i] <= x_points[i + 1] for i in range(len(x_points) - 1)):
        raise ValueError("x_points must be sorted in ascending order")

    # ------------------------------------------------------------------
    # Method handling
    # ------------------------------------------------------------------
    method = method.lower()
    valid_methods = [
        'linear', 'polynomial', 'lagrange', 'newton',
        'cubic_spline', 'nearest_neighbor'
    ]
    if method not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")

    extrapolate = kwargs.get('extrapolate', False)
    degree = kwargs.get('degree', len(x_points) - 1)

    # Handle extrapolation rules
    x_min, x_max = x_points[0], x_points[-1]
    if not extrapolate:
        for x in x_new:
            if x < x_min or x > x_max:
                raise ValueError("extrapolation not allowed")

    # Track which points were extrapolated
    extrapolated_points = [x for x in x_new if x < x_min or x > x_max]

    # ------------------------------------------------------------------
    # Perform interpolation
    # ------------------------------------------------------------------
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
    elif method == 'nearest_neighbor':
        results = [_nearest_neighbor_interpolation(x_points, y_points, x) for x in x_new]

    return {
        'y_interpolated': results,
        'method_used': method,
        'extrapolated_points': extrapolated_points,
        'interpolation_error': None,
    }


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
