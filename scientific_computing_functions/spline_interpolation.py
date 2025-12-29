"""
Perform spline interpolation with validation.

Uses scipy.interpolate, adds validation, multiple spline types,
and comprehensive interpolation output.
"""

from typing import Literal

import numpy as np
from scipy import interpolate


def spline_interpolation(
    x: list[float] | np.ndarray,
    y: list[float] | np.ndarray,
    x_new: list[float] | np.ndarray,
    kind: Literal["linear", "cubic", "quintic"] = "cubic",
    extrapolate: bool = False,
) -> dict[str, np.ndarray]:
    """
    Perform spline interpolation with validation.

    Uses scipy.interpolate, adds validation, multiple spline types,
    and comprehensive interpolation output.

    Parameters
    ----------
    x : list[float] | np.ndarray
        Known data points (x-coordinates).
    y : list[float] | np.ndarray
        Known data points (y-coordinates).
    x_new : list[float] | np.ndarray
        Points to interpolate at.
    kind : {'linear', 'cubic', 'quintic'}, optional
        Interpolation method (by default 'cubic').
    extrapolate : bool, optional
        Whether to extrapolate outside data range (by default False).

    Returns
    -------
    dict[str, np.ndarray]
        Dictionary containing:
        - x_new: Interpolation points
        - y_new: Interpolated values
        - spline: Interpolation function object

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is invalid or interpolation fails.

    Examples
    --------
    >>> x = [0, 1, 2, 3, 4]
    >>> y = [0, 1, 4, 9, 16]
    >>> x_new = [0.5, 1.5, 2.5]
    >>> result = spline_interpolation(x, y, x_new, kind='cubic')
    >>> len(result['y_new'])
    3

    Notes
    -----
    - Linear: Piecewise linear, C⁰ continuous
    - Cubic: Smooth, C² continuous
    - Quintic: Very smooth, C⁴ continuous

    Complexity
    ----------
    Time: O(n log n) for setup, O(log n) per evaluation
    Space: O(n)
    """
    # Input validation
    if not isinstance(x, (list, np.ndarray)):
        raise TypeError(f"x must be a list or numpy array, got {type(x).__name__}")
    if not isinstance(y, (list, np.ndarray)):
        raise TypeError(f"y must be a list or numpy array, got {type(y).__name__}")
    if not isinstance(x_new, (list, np.ndarray)):
        raise TypeError(
            f"x_new must be a list or numpy array, got {type(x_new).__name__}"
        )
    if not isinstance(kind, str):
        raise TypeError(f"kind must be a string, got {type(kind).__name__}")
    if kind not in ("linear", "cubic", "quintic"):
        raise ValueError(
            f"kind must be 'linear', 'cubic', or 'quintic', got '{kind}'"
        )
    if not isinstance(extrapolate, bool):
        raise TypeError(
            f"extrapolate must be a boolean, got {type(extrapolate).__name__}"
        )

    # Convert to numpy arrays
    try:
        x_arr = np.asarray(x, dtype=float)
        y_arr = np.asarray(y, dtype=float)
        x_new_arr = np.asarray(x_new, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"arrays contain non-numeric values: {e}") from e

    if x_arr.ndim != 1:
        raise ValueError(f"x must be 1-dimensional, got {x_arr.ndim} dimensions")
    if y_arr.ndim != 1:
        raise ValueError(f"y must be 1-dimensional, got {y_arr.ndim} dimensions")
    if x_new_arr.ndim != 1:
        raise ValueError(f"x_new must be 1-dimensional, got {x_new_arr.ndim} dimensions")
    if x_arr.size != y_arr.size:
        raise ValueError(
            f"x and y must have same length, got {x_arr.size} and {y_arr.size}"
        )
    if x_arr.size < 2:
        raise ValueError(f"need at least 2 data points, got {x_arr.size}")
    if x_new_arr.size == 0:
        raise ValueError("x_new cannot be empty")

    if np.any(~np.isfinite(x_arr)):
        raise ValueError("x contains NaN or Inf values")
    if np.any(~np.isfinite(y_arr)):
        raise ValueError("y contains NaN or Inf values")
    if np.any(~np.isfinite(x_new_arr)):
        raise ValueError("x_new contains NaN or Inf values")

    # Check if x is monotonically increasing (required for interpolation)
    if not np.all(np.diff(x_arr) > 0):
        # Sort by x
        sort_idx = np.argsort(x_arr)
        x_arr = x_arr[sort_idx]
        y_arr = y_arr[sort_idx]

        # Check again after sorting
        if not np.all(np.diff(x_arr) > 0):
            raise ValueError("x values must be unique and monotonically increasing")

    # Check minimum points for spline type
    min_points = {"linear": 2, "cubic": 4, "quintic": 6}
    if x_arr.size < min_points[kind]:
        raise ValueError(
            f"{kind} interpolation requires at least {min_points[kind]} points, got {x_arr.size}"
        )

    # Check extrapolation bounds
    if not extrapolate:
        x_min, x_max = x_arr[0], x_arr[-1]
        if np.any((x_new_arr < x_min) | (x_new_arr > x_max)):
            raise ValueError(
                f"x_new contains values outside data range [{x_min}, {x_max}] and extrapolate=False"
            )

    # Create interpolation function
    try:
        if kind == "linear":
            spline = interpolate.interp1d(
                x_arr, y_arr, kind="linear", fill_value="extrapolate" if extrapolate else np.nan
            )
        elif kind == "cubic":
            spline = interpolate.CubicSpline(
                x_arr, y_arr, extrapolate=extrapolate
            )
        elif kind == "quintic":
            # Use make_interp_spline for quintic
            spline = interpolate.make_interp_spline(
                x_arr, y_arr, k=5, extrapolate=extrapolate
            )
        else:
            raise ValueError(f"Unknown kind: {kind}")
    except Exception as e:
        raise ValueError(f"spline creation failed: {e}") from e

    # Evaluate spline
    try:
        y_new = spline(x_new_arr)
    except Exception as e:
        raise ValueError(f"spline evaluation failed: {e}") from e

    return {
        "x_new": x_new_arr,
        "y_new": y_new,
        "spline": spline,
    }


__all__ = ["spline_interpolation"]
