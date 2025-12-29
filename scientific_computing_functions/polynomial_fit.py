"""
Perform polynomial curve fitting with validation.

Uses numpy.polyfit, adds validation, residual analysis,
and comprehensive fitting output.
"""

import numpy as np


def polynomial_fit(
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
    degree: int,
    return_residuals: bool = True,
    return_coefficients_cov: bool = False,
) -> dict[str, np.ndarray | float]:
    """
    Perform polynomial curve fitting with validation.

    Uses numpy.polyfit, adds validation, residual analysis,
    and comprehensive fitting output.

    Parameters
    ----------
    x : list[float] | np.ndarray
        Independent variable data.
    y : list[float] | np.ndarray
        Dependent variable data.
    degree : int
        Degree of polynomial to fit.
    return_residuals : bool, optional
        Whether to compute residuals and R² (by default True).
    return_coefficients_cov : bool, optional
        Whether to return covariance matrix (by default False).

    Returns
    -------
    dict[str, np.ndarray | float]
        Dictionary containing:
        - coefficients: Polynomial coefficients (highest degree first)
        - polynomial: np.poly1d object for evaluation
        - residuals: Sum of squared residuals (if requested)
        - r_squared: R² value (if requested)
        - covariance: Covariance matrix (if requested)

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is invalid or degree is negative.

    Examples
    --------
    >>> x = [0, 1, 2, 3, 4]
    >>> y = [0, 1, 4, 9, 16]  # y = x^2
    >>> result = polynomial_fit(x, y, degree=2)
    >>> result['r_squared'] > 0.99
    True

    Notes
    -----
    Higher degree polynomials may overfit the data.
    Consider cross-validation for model selection.

    Complexity
    ----------
    Time: O(n * d²), Space: O(d²)
    """
    # Input validation
    if not isinstance(x, (list, np.ndarray)):
        raise TypeError(f"x must be a list or numpy array, got {type(x).__name__}")
    if not isinstance(y, (list, np.ndarray)):
        raise TypeError(f"y must be a list or numpy array, got {type(y).__name__}")
    if not isinstance(degree, int):
        raise TypeError(f"degree must be an integer, got {type(degree).__name__}")
    if degree < 0:
        raise ValueError(f"degree must be non-negative, got {degree}")
    if not isinstance(return_residuals, bool):
        raise TypeError(
            f"return_residuals must be a boolean, got {type(return_residuals).__name__}"
        )
    if not isinstance(return_coefficients_cov, bool):
        raise TypeError(
            f"return_coefficients_cov must be a boolean, got {type(return_coefficients_cov).__name__}"
        )

    # Convert to numpy arrays
    try:
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"arrays contain non-numeric values: {e}") from e

    if x_arr.ndim != 1:
        raise ValueError(f"x must be 1-dimensional, got {x_arr.ndim} dimensions")
    if y_arr.ndim != 1:
        raise ValueError(f"y must be 1-dimensional, got {y_arr.ndim} dimensions")
    if x_arr.size != y_arr.size:
        raise ValueError(
            f"x and y must have same length, got {x_arr.size} and {y_arr.size}"
        )
    if x_arr.size <= degree:
        raise ValueError(
            f"need more data points than degree, got {x_arr.size} points for degree {degree}"
        )

    if np.any(~np.isfinite(x_arr)):
        raise ValueError("x contains NaN or Inf values")
    if np.any(~np.isfinite(y_arr)):
        raise ValueError("y contains NaN or Inf values")

    # Fit polynomial
    try:
        if return_coefficients_cov:
            coeffs, cov = np.polyfit(x_arr, y_arr, degree, cov=True)
        else:
            coeffs = np.polyfit(x_arr, y_arr, degree)
            cov = None
    except Exception as e:
        raise ValueError(f"polynomial fitting failed: {e}") from e

    # Create polynomial object
    poly = np.poly1d(coeffs)

    result = {
        "coefficients": coeffs,
        "polynomial": poly,
    }

    # Compute residuals and R²
    if return_residuals:
        y_pred = poly(x_arr)
        residuals = y_arr - y_pred
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_arr - np.mean(y_arr)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

        result["residuals"] = float(ss_res)
        result["r_squared"] = float(r_squared)

    if cov is not None:
        result["covariance"] = cov

    return result


__all__ = ["polynomial_fit"]
