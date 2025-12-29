"""
Perform chi-square goodness-of-fit test.

Uses scipy.stats.chisquare, adds validation and interpretation.
"""

import numpy as np
from scipy import stats


def perform_chi_square_test(
    observed: list[int] | np.ndarray,
    expected: list[int] | np.ndarray | None = None,
    alpha: float = 0.05,
) -> dict[str, float | bool]:
    """
    Perform chi-square goodness-of-fit test.

    Uses scipy.stats.chisquare, adds validation and interpretation.

    Parameters
    ----------
    observed : list[int] | np.ndarray
        Observed frequencies.
    expected : list[int] | np.ndarray | None, optional
        Expected frequencies (by default None, assumes uniform).
    alpha : float, optional
        Significance level (by default 0.05).

    Returns
    -------
    dict[str, float | bool]
        Dictionary containing:
        - statistic: Chi-square statistic
        - pvalue: p-value
        - significant: Whether result is significant
        - degrees_of_freedom: Degrees of freedom

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If observed is empty or contains negative values.

    Examples
    --------
    >>> observed = [10, 15, 20, 15]
    >>> result = perform_chi_square_test(observed)
    >>> 'pvalue' in result
    True

    Notes
    -----
    Tests whether observed frequencies differ significantly from expected.

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    # Input validation
    if not isinstance(observed, (list, np.ndarray)):
        raise TypeError(
            f"observed must be a list or numpy array, got {type(observed).__name__}"
        )
    if expected is not None and not isinstance(expected, (list, np.ndarray)):
        raise TypeError(
            f"expected must be a list, numpy array, or None, got {type(expected).__name__}"
        )
    if not isinstance(alpha, (int, float)):
        raise TypeError(f"alpha must be a number, got {type(alpha).__name__}")
    if alpha <= 0 or alpha >= 1:
        raise ValueError(f"alpha must be between 0 and 1, got {alpha}")

    # Convert to numpy arrays
    try:
        obs_arr = np.asarray(observed, dtype=float)
        exp_arr = np.asarray(expected, dtype=float) if expected is not None else None
    except (ValueError, TypeError) as e:
        raise ValueError(f"arrays contain non-numeric values: {e}") from e

    if obs_arr.size == 0:
        raise ValueError("observed cannot be empty")
    if np.any(obs_arr < 0):
        raise ValueError("observed frequencies cannot be negative")
    if exp_arr is not None and np.any(exp_arr < 0):
        raise ValueError("expected frequencies cannot be negative")

    # Perform chi-square test
    chi2_stat, p_value = stats.chisquare(obs_arr, exp_arr)

    # Degrees of freedom
    df = obs_arr.size - 1

    return {
        "statistic": float(chi2_stat),
        "pvalue": float(p_value),
        "significant": p_value < alpha,
        "degrees_of_freedom": int(df),
        "alpha": alpha,
    }


__all__ = ["perform_chi_square_test"]
