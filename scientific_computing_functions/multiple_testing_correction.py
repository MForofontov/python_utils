"""
Apply multiple testing correction to p-values.

Implements correction methods (Bonferroni, Holm, FDR), adds validation
and comprehensive reporting.
"""

from typing import Literal

import numpy as np


def multiple_testing_correction(
    pvalues: list[float] | np.ndarray,
    method: Literal["bonferroni", "holm", "fdr_bh"] = "fdr_bh",
    alpha: float = 0.05,
) -> dict[str, np.ndarray | list[bool] | float]:
    """
    Apply multiple testing correction to p-values.

    Implements correction methods, adds validation and comprehensive reporting.

    Parameters
    ----------
    pvalues : list[float] | np.ndarray
        Array of p-values to correct.
    method : {'bonferroni', 'holm', 'fdr_bh'}, optional
        Correction method (by default 'fdr_bh').
        - bonferroni: Bonferroni correction
        - holm: Holm-Bonferroni sequential method
        - fdr_bh: Benjamini-Hochberg FDR control
    alpha : float, optional
        Family-wise error rate or FDR level (by default 0.05).

    Returns
    -------
    dict[str, np.ndarray | list[bool] | float]
        Dictionary containing:
        - corrected_pvalues: Adjusted p-values
        - rejected: Boolean array of rejected hypotheses
        - n_rejected: Number of rejected hypotheses
        - correction_method: Method used

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If pvalues is empty or contains invalid values.

    Examples
    --------
    >>> pvalues = [0.01, 0.04, 0.03, 0.50]
    >>> result = multiple_testing_correction(pvalues, method='bonferroni')
    >>> result['n_rejected']
    1

    Notes
    -----
    - Bonferroni: Most conservative, controls FWER
    - Holm: Less conservative than Bonferroni
    - FDR BH: Controls false discovery rate, more powerful

    Complexity
    ----------
    Time: O(n log n), Space: O(n)
    """
    # Input validation
    if not isinstance(pvalues, (list, np.ndarray)):
        raise TypeError(
            f"pvalues must be a list or numpy array, got {type(pvalues).__name__}"
        )
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}")
    if method not in ("bonferroni", "holm", "fdr_bh"):
        raise ValueError(
            f"method must be 'bonferroni', 'holm', or 'fdr_bh', got '{method}'"
        )
    if not isinstance(alpha, (int, float)):
        raise TypeError(f"alpha must be a number, got {type(alpha).__name__}")
    if alpha <= 0 or alpha >= 1:
        raise ValueError(f"alpha must be between 0 and 1, got {alpha}")

    # Convert to numpy array
    try:
        pvals = np.asarray(pvalues, dtype=float)
    except (ValueError, TypeError) as e:
        raise ValueError(f"pvalues contain non-numeric values: {e}") from e

    if pvals.size == 0:
        raise ValueError("pvalues cannot be empty")
    if np.any((pvals < 0) | (pvals > 1)):
        raise ValueError("all p-values must be between 0 and 1")

    n = pvals.size

    if method == "bonferroni":
        # Bonferroni correction
        corrected = np.minimum(pvals * n, 1.0)
        rejected = corrected < alpha

    elif method == "holm":
        # Holm-Bonferroni method
        sorted_idx = np.argsort(pvals)
        sorted_pvals = pvals[sorted_idx]
        corrected = np.zeros(n)

        for i in range(n):
            corrected[sorted_idx[i]] = min(max(sorted_pvals[i] * (n - i), 1.0), 1.0)

        rejected = corrected < alpha

    elif method == "fdr_bh":
        # Benjamini-Hochberg FDR control
        sorted_idx = np.argsort(pvals)
        sorted_pvals = pvals[sorted_idx]
        corrected = np.zeros(n)

        for i in range(n):
            corrected[sorted_idx[i]] = min(sorted_pvals[i] * n / (i + 1), 1.0)

        # Make monotone
        for i in range(n - 1, 0, -1):
            if corrected[sorted_idx[i]] < corrected[sorted_idx[i - 1]]:
                corrected[sorted_idx[i - 1]] = corrected[sorted_idx[i]]

        rejected = corrected < alpha

    else:
        raise ValueError(f"Unknown method: {method}")

    return {
        "corrected_pvalues": corrected,
        "rejected": rejected.tolist(),
        "n_rejected": int(np.sum(rejected)),
        "n_total": int(n),
        "correction_method": method,
        "alpha": alpha,
    }


__all__ = ["multiple_testing_correction"]
