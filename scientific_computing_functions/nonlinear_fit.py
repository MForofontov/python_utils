"""
Perform nonlinear curve fitting with validation.

Uses scipy.optimize.curve_fit, adds validation, confidence intervals,
and comprehensive fitting output.
"""

from typing import Callable

import numpy as np
from scipy import optimize


def nonlinear_fit(
    func: Callable,
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
    p0: list[float] | np.ndarray | None = None,
    bounds: tuple | None = None,
    sigma: list[float] | np.ndarray | None = None,
    absolute_sigma: bool = False,
    **kwargs,
) -> dict[str, np.ndarray | float | bool]:
    """
    Perform nonlinear curve fitting with validation.

    Uses scipy.optimize.curve_fit, adds validation, confidence intervals,
    and comprehensive fitting output.

    Parameters
    ----------
    func : Callable
        Model function: func(x, *params) -> y.
    x : list[float] | np.ndarray
        Independent variable data.
    y : list[float] | np.ndarray
        Dependent variable data.
    p0 : list[float] | np.ndarray | None, optional
        Initial parameter guesses (by default None).
    bounds : tuple | None, optional
        Parameter bounds as (lower, upper) (by default None).
    sigma : list[float] | np.ndarray | None, optional
        Uncertainties in y values (by default None).
    absolute_sigma : bool, optional
        If True, sigma is absolute, else relative (by default False).
    **kwargs
        Additional arguments for curve_fit.

    Returns
    -------
    dict[str, np.ndarray | float | bool]
        Dictionary containing:
        - parameters: Optimal parameter values
        - covariance: Parameter covariance matrix
        - standard_errors: Standard errors of parameters
        - residuals: Sum of squared residuals
        - r_squared: R² value
        - success: Whether fitting succeeded

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is invalid or fitting fails.

    Examples
    --------
    >>> def exponential(x, a, b):
    ...     return a * np.exp(b * x)
    >>> x = [0, 1, 2, 3]
    >>> y = [1.0, 2.7, 7.4, 20.1]
    >>> result = nonlinear_fit(exponential, x, y, p0=[1, 1])
    >>> result['success']
    True

    Notes
    -----
    Requires good initial parameter guesses for convergence.
    May converge to local minimum instead of global.

    Complexity
    ----------
    Time: Depends on problem complexity, Space: O(n * p)
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(x, (list, np.ndarray)):
        raise TypeError(f"x must be a list or numpy array, got {type(x).__name__}")
    if not isinstance(y, (list, np.ndarray)):
        raise TypeError(f"y must be a list or numpy array, got {type(y).__name__}")
    if p0 is not None and not isinstance(p0, (list, np.ndarray)):
        raise TypeError(
            f"p0 must be a list, numpy array, or None, got {type(p0).__name__}"
        )
    if sigma is not None and not isinstance(sigma, (list, np.ndarray)):
        raise TypeError(
            f"sigma must be a list, numpy array, or None, got {type(sigma).__name__}"
        )
    if not isinstance(absolute_sigma, bool):
        raise TypeError(
            f"absolute_sigma must be a boolean, got {type(absolute_sigma).__name__}"
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
    if x_arr.size == 0:
        raise ValueError("x and y cannot be empty")

    if np.any(~np.isfinite(x_arr)):
        raise ValueError("x contains NaN or Inf values")
    if np.any(~np.isfinite(y_arr)):
        raise ValueError("y contains NaN or Inf values")

    # Validate p0
    if p0 is not None:
        try:
            p0_arr = np.asarray(p0, dtype=float)
        except (ValueError, TypeError) as e:
            raise ValueError(f"p0 contains non-numeric values: {e}") from e
        if np.any(~np.isfinite(p0_arr)):
            raise ValueError("p0 contains NaN or Inf values")
    else:
        p0_arr = None

    # Validate sigma
    if sigma is not None:
        try:
            sigma_arr = np.asarray(sigma, dtype=float)
        except (ValueError, TypeError) as e:
            raise ValueError(f"sigma contains non-numeric values: {e}") from e
        if sigma_arr.size != y_arr.size:
            raise ValueError(
                f"sigma must have same length as y, got {sigma_arr.size} and {y_arr.size}"
            )
        if np.any(sigma_arr <= 0):
            raise ValueError("sigma values must be positive")
    else:
        sigma_arr = None

    # Perform curve fitting
    try:
        popt, pcov = optimize.curve_fit(
            func,
            x_arr,
            y_arr,
            p0=p0_arr,
            sigma=sigma_arr,
            absolute_sigma=absolute_sigma,
            bounds=bounds if bounds is not None else (-np.inf, np.inf),
            **kwargs,
        )
        success = True
    except Exception as e:
        raise ValueError(f"curve fitting failed: {e}") from e

    # Compute standard errors
    perr = np.sqrt(np.diag(pcov))

    # Compute residuals and R²
    y_pred = func(x_arr, *popt)
    residuals = y_arr - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_arr - np.mean(y_arr)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    return {
        "parameters": popt,
        "covariance": pcov,
        "standard_errors": perr,
        "residuals": float(ss_res),
        "r_squared": float(r_squared),
        "success": success,
    }


__all__ = ["nonlinear_fit"]
