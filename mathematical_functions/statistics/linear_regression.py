"""Perform linear regression analysis."""

from typing import Union, Dict
import math


def linear_regression(x: list[Union[int, float]], y: list[Union[int, float]]) -> Dict[str, float]:
    """
    Perform simple linear regression analysis (y = ax + b).

    Parameters
    ----------
    x : list[int | float]
        Independent variable values.
    y : list[int | float] 
        Dependent variable values (must be same length as x).

    Returns
    -------
    dict[str, float]
        Dictionary containing regression results:
        - 'slope': Slope coefficient (a)
        - 'intercept': Y-intercept coefficient (b)
        - 'r_squared': Coefficient of determination (R²)
        - 'correlation': Correlation coefficient (r)
        - 'std_error_slope': Standard error of slope
        - 'std_error_intercept': Standard error of intercept

    Raises
    ------
    TypeError
        If x or y is not a list or contains non-numeric values.
    ValueError
        If x and y have different lengths or fewer than 2 elements.

    Examples
    --------
    >>> result = linear_regression([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    >>> abs(result['slope'] - 2.0) < 1e-10
    True
    >>> abs(result['intercept'] - 0.0) < 1e-10
    True
    >>> abs(result['r_squared'] - 1.0) < 1e-10
    True
    """
    # Input validation
    if not isinstance(x, list):
        raise TypeError("x must be a list")
    
    if not isinstance(y, list):
        raise TypeError("y must be a list")
    
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    if len(x) < 2:
        raise ValueError("linear regression requires at least 2 values")

    # Ensure all values are numeric
    if not all(isinstance(val, (int, float)) for val in x + y):
        raise TypeError("all values must be numeric")
    
    n = len(x)
    
    # Calculate means
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Calculate sums of squares and cross products
    ss_xx = sum((xi - mean_x) ** 2 for xi in x)
    ss_yy = sum((yi - mean_y) ** 2 for yi in y)
    ss_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    
    # Handle perfect vertical line case
    if ss_xx == 0:
        if ss_yy == 0:
            # Both x and y are constant
            return {
                'slope': 0.0,
                'intercept': mean_y,
                'r_squared': 1.0,
                'correlation': 1.0,
                'std_error_slope': 0.0,
                'std_error_intercept': 0.0,
                'p_value': 0.0
            }
        else:
            raise ValueError("x values must have variation for regression analysis")
    
    # Calculate regression coefficients
    slope = ss_xy / ss_xx
    intercept = mean_y - slope * mean_x
    
    # Calculate correlation coefficient
    if ss_yy == 0:
        correlation = 1.0 if slope == 0 else 0.0
    else:
        correlation = ss_xy / math.sqrt(ss_xx * ss_yy)
    
    # Calculate R-squared
    r_squared = correlation ** 2
    
    # Calculate residuals and standard errors
    y_predicted = [slope * xi + intercept for xi in x]
    residuals = [y[i] - y_predicted[i] for i in range(n)]
    
    # Mean squared error of residuals
    if n > 2:
        mse_residual = sum(r ** 2 for r in residuals) / (n - 2)

        # Standard errors
        std_error_slope = math.sqrt(mse_residual / ss_xx) if ss_xx > 0 else 0.0
        std_error_intercept = math.sqrt(mse_residual * (1 / n + mean_x**2 / ss_xx))

        # Compute p-value using normal approximation for two-tailed test
        if std_error_slope > 0:
            t_stat = slope / std_error_slope
            # CDF of standard normal distribution
            p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / math.sqrt(2))))
        else:
            p_value = 0.0
    else:
        std_error_slope = 0.0
        std_error_intercept = 0.0
        p_value = 0.0

    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'correlation': correlation,
        'std_error_slope': std_error_slope,
        'std_error_intercept': std_error_intercept,
        'p_value': p_value
    }


def predict_linear(x_values: list[Union[int, float]], slope: float, intercept: float) -> list[float]:
    """
    Make predictions using linear regression coefficients.

    Parameters
    ----------
    x_values : list[int | float]
        X values for prediction.
    slope : float
        Slope coefficient from linear regression.
    intercept : float
        Intercept coefficient from linear regression.

    Returns
    -------
    list[float]
        Predicted y values.

    Raises
    ------
    TypeError
        If inputs are not of correct types.

    Examples
    --------
    >>> predict_linear([6, 7, 8], 2.0, 0.0)
    [12.0, 14.0, 16.0]
    """
    if not isinstance(x_values, list):
        raise TypeError("x_values must be a list")
    
    if not isinstance(slope, (int, float)):
        raise TypeError("slope must be numeric")
    
    if not isinstance(intercept, (int, float)):
        raise TypeError("intercept must be numeric")
    
    if not all(isinstance(val, (int, float)) for val in x_values):
        raise TypeError("all values in x_values must be numeric")
    
    return [slope * x + intercept for x in x_values]


__all__ = ['linear_regression', 'predict_linear']
