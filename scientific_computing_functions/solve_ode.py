"""
Solve ordinary differential equation (ODE) with validation.

Uses scipy.integrate.solve_ivp, adds validation, method selection,
and comprehensive solution output.
"""

from typing import Callable

import numpy as np
from scipy import integrate


def solve_ode(
    func: Callable[[float, np.ndarray], np.ndarray],
    t_span: tuple[float, float],
    y0: list[float] | np.ndarray,
    method: str = "RK45",
    t_eval: list[float] | np.ndarray | None = None,
    dense_output: bool = False,
    **kwargs,
) -> dict[str, np.ndarray | bool]:
    """
    Solve ordinary differential equation (ODE) with validation.

    Uses scipy.integrate.solve_ivp, adds validation and comprehensive output.

    Parameters
    ----------
    func : Callable[[float, np.ndarray], np.ndarray]
        Function computing dy/dt. Signature: func(t, y) -> dy/dt.
    t_span : tuple[float, float]
        Interval of integration (t0, tf).
    y0 : list[float] | np.ndarray
        Initial state.
    method : str, optional
        Integration method (by default 'RK45').
        Options: 'RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA'.
    t_eval : list[float] | np.ndarray | None, optional
        Times at which to store solution (by default None).
    dense_output : bool, optional
        Whether to compute continuous solution (by default False).
    **kwargs
        Additional arguments for solve_ivp.

    Returns
    -------
    dict[str, np.ndarray | bool]
        Dictionary containing:
        - t: Time points
        - y: Solution values at each time point
        - success: Whether integration was successful
        - message: Status message

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters are invalid or integration fails.

    Examples
    --------
    >>> def exponential_growth(t, y):
    ...     return y  # dy/dt = y, solution: y = y0 * exp(t)
    >>> result = solve_ode(exponential_growth, (0, 1), [1.0])
    >>> result['success']
    True

    Notes
    -----
    - RK45: Good default, 4th/5th order Runge-Kutta
    - BDF: For stiff problems
    - LSODA: Automatically switches between stiff/non-stiff

    Complexity
    ----------
    Time: Depends on problem and method, Space: O(n * m)
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(t_span, (tuple, list)):
        raise TypeError(
            f"t_span must be a tuple or list, got {type(t_span).__name__}"
        )
    if len(t_span) != 2:
        raise ValueError(f"t_span must have 2 elements, got {len(t_span)}")
    if not isinstance(y0, (list, np.ndarray)):
        raise TypeError(
            f"y0 must be a list or numpy array, got {type(y0).__name__}"
        )
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}")
    if method not in ("RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"):
        raise ValueError(
            f"method must be 'RK45', 'RK23', 'DOP853', 'Radau', 'BDF', or 'LSODA', got '{method}'"
        )
    if not isinstance(dense_output, bool):
        raise TypeError(
            f"dense_output must be a boolean, got {type(dense_output).__name__}"
        )

    # Validate t_span
    try:
        t0, tf = float(t_span[0]), float(t_span[1])
    except (ValueError, TypeError) as e:
        raise ValueError(f"t_span elements must be numeric: {e}") from e

    if not np.isfinite(t0) or not np.isfinite(tf):
        raise ValueError("t_span elements must be finite")
    if t0 >= tf:
        raise ValueError(f"t_span[0] must be < t_span[1], got {t0} >= {tf}")

    # Validate y0
    try:
        y0_arr = np.asarray(y0, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"y0 contains non-numeric values: {e}") from e

    if y0_arr.size == 0:
        raise ValueError("y0 cannot be empty")
    if np.any(~np.isfinite(y0_arr)):
        raise ValueError("y0 contains NaN or Inf values")

    # Validate t_eval if provided
    if t_eval is not None:
        if not isinstance(t_eval, (list, np.ndarray)):
            raise TypeError(
                f"t_eval must be a list, numpy array, or None, got {type(t_eval).__name__}"
            )
        try:
            t_eval_arr = np.asarray(t_eval, dtype=float)
        except (ValueError, TypeError) as e:
            raise ValueError(f"t_eval contains non-numeric values: {e}") from e

        if t_eval_arr.size == 0:
            raise ValueError("t_eval cannot be empty")
        if np.any(~np.isfinite(t_eval_arr)):
            raise ValueError("t_eval contains NaN or Inf values")
    else:
        t_eval_arr = None

    # Solve ODE
    try:
        sol = integrate.solve_ivp(
            func,
            (t0, tf),
            y0_arr,
            method=method,
            t_eval=t_eval_arr,
            dense_output=dense_output,
            **kwargs,
        )
    except Exception as e:
        raise ValueError(f"ODE integration failed: {e}") from e

    return {
        "t": sol.t,
        "y": sol.y,
        "success": bool(sol.success),
        "message": sol.message,
        "nfev": int(sol.nfev) if hasattr(sol, "nfev") else None,
        "njev": int(sol.njev) if hasattr(sol, "njev") else None,
    }


__all__ = ["solve_ode"]
