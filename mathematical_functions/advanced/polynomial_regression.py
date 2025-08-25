"""Perform polynomial regression analysis with multiple degrees."""

from typing import Union, List, Tuple, Dict
import math


def polynomial_regression(x: list[Union[int, float]], 
                         y: list[Union[int, float]], 
                         degree: int) -> Dict[str, Union[List[float], float]]:
    """
    Perform polynomial regression analysis using least squares method.

    Fits a polynomial of specified degree: y = a₀ + a₁x + a₂x² + ... + aₙxⁿ
    Uses matrix operations to solve the normal equations.

    Parameters
    ----------
    x : list[int | float]
        Independent variable values.
    y : list[int | float]
        Dependent variable values (must be same length as x).
    degree : int
        Degree of polynomial (must be positive and < len(x)).

    Returns
    -------
    dict[str, Union[List[float], float]]
        Dictionary containing:
        - 'coefficients': List of coefficients [a₀, a₁, a₂, ..., aₙ]
        - 'r_squared': Coefficient of determination
        - 'residual_sum_squares': Sum of squared residuals
        - 'total_sum_squares': Total sum of squares
        - 'standard_error': Standard error of estimate
        - 'condition_number': Matrix condition number (numerical stability)

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If data validation fails or matrix is singular.

    Examples
    --------
    >>> # Quadratic fit
    >>> result = polynomial_regression([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], 2)
    >>> len(result['coefficients'])
    3
    >>> result['r_squared'] > 0.99
    True
    """
    # Comprehensive input validation
    if not isinstance(x, list):
        raise TypeError("x must be a list")
    if not isinstance(y, list):
        raise TypeError("y must be a list")
    if not isinstance(degree, int):
        raise TypeError("degree must be an integer")
    
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 2:
        raise ValueError("need at least 2 data points")
    if degree < 1:
        raise ValueError("degree must be at least 1")
    if degree >= len(x):
        raise ValueError("degree must be less than number of data points")
    
    if not all(isinstance(val, (int, float)) for val in x):
        raise TypeError("all values in x must be numeric")
    if not all(isinstance(val, (int, float)) for val in y):
        raise TypeError("all values in y must be numeric")
    
    # Check for duplicate x values that could cause numerical issues
    x_set = set(x)
    if len(x_set) != len(x):
        raise ValueError("x values must be unique for stable polynomial fitting")
    
    n = len(x)
    
    # Build Vandermonde matrix A where A[i,j] = x[i]^j
    A = []
    for i in range(n):
        row = []
        for j in range(degree + 1):
            row.append(x[i] ** j)
        A.append(row)
    
    # Build normal equations: A^T * A * coeffs = A^T * y
    # First compute A^T * A
    AtA = []
    for i in range(degree + 1):
        row = []
        for j in range(degree + 1):
            sum_val = sum(A[k][i] * A[k][j] for k in range(n))
            row.append(sum_val)
        AtA.append(row)
    
    # Compute A^T * y
    Aty = []
    for i in range(degree + 1):
        sum_val = sum(A[k][i] * y[k] for k in range(n))
        Aty.append(sum_val)
    
    # Check condition number for numerical stability
    try:
        condition_number = _matrix_condition_number(AtA)
        if condition_number > 1e12:
            raise ValueError(f"Matrix is ill-conditioned (condition number: {condition_number:.2e})")
    except:
        condition_number = float('inf')
    
    # Solve linear system AtA * coeffs = Aty using Gaussian elimination
    try:
        coefficients = _gaussian_elimination(AtA, Aty)
    except Exception as e:
        raise ValueError(f"Failed to solve normal equations: {str(e)}")
    
    # Calculate predictions and residuals
    y_pred = []
    for xi in x:
        pred = sum(coefficients[j] * (xi ** j) for j in range(degree + 1))
        y_pred.append(pred)
    
    residuals = [y[i] - y_pred[i] for i in range(n)]
    
    # Calculate goodness of fit metrics
    y_mean = sum(y) / n
    total_sum_squares = sum((yi - y_mean) ** 2 for yi in y)
    residual_sum_squares = sum(r ** 2 for r in residuals)
    
    # Handle edge cases
    if total_sum_squares == 0:
        r_squared = 1.0 if residual_sum_squares < 1e-10 else 0.0
    else:
        r_squared = 1.0 - (residual_sum_squares / total_sum_squares)
    
    # Standard error of estimate
    if n > degree + 1:
        standard_error = math.sqrt(residual_sum_squares / (n - degree - 1))
    else:
        standard_error = 0.0
    
    return {
        'coefficients': coefficients,
        'r_squared': r_squared,
        'residual_sum_squares': residual_sum_squares,
        'total_sum_squares': total_sum_squares,
        'standard_error': standard_error,
        'condition_number': condition_number
    }


def _gaussian_elimination(A: List[List[float]], b: List[float]) -> List[float]:
    """Solve Ax = b using Gaussian elimination with partial pivoting."""
    n = len(A)
    
    # Create augmented matrix
    augmented = []
    for i in range(n):
        row = A[i][:] + [b[i]]
        augmented.append(row)
    
    # Forward elimination with partial pivoting
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        
        if abs(augmented[max_row][i]) < 1e-12:
            raise ValueError("Matrix is singular or near-singular")
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            factor = augmented[k][i] / augmented[i][i]
            for j in range(i, n + 1):
                augmented[k][j] -= factor * augmented[i][j]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]
    
    return x


def _matrix_condition_number(A: List[List[float]]) -> float:
    """Estimate condition number using simple eigenvalue bounds."""
    n = len(A)
    if n == 0:
        return 1.0
    
    # Simple estimation using diagonal dominance and Gershgorin circles
    min_diag = min(abs(A[i][i]) for i in range(n))
    max_sum = max(sum(abs(A[i][j]) for j in range(n)) for i in range(n))
    
    if min_diag < 1e-12:
        return float('inf')
    
    return max_sum / min_diag


__all__ = ['polynomial_regression']
