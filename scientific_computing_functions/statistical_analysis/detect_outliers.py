"""Detect outliers using multiple methods and return consensus results."""

from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray
from scipy import stats


def detect_outliers(
    data: list[float] | NDArray[Any],
    methods: list[Literal["zscore", "iqr", "mad", "isolation"]] | None = None,
    zscore_threshold: float = 3.0,
    iqr_multiplier: float = 1.5,
    mad_threshold: float = 3.5,
    consensus_threshold: float = 0.5,
) -> dict[str, Any]:
    """
    Detect outliers using multiple methods and return consensus results.

    Combines Z-score, IQR, MAD, and isolation forest methods to identify outliers
    with a consensus approach. This provides more robust outlier detection than
    any single method.

    Parameters
    ----------
    data : list[float] | NDArray[Any]
        Input data array.
    methods : list[Literal["zscore", "iqr", "mad", "isolation"]] | None, optional
        Methods to use for outlier detection (by default ["zscore", "iqr", "mad"]).
    zscore_threshold : float, optional
        Z-score threshold for outlier detection (by default 3.0).
    iqr_multiplier : float, optional
        IQR multiplier for outlier detection (by default 1.5).
    mad_threshold : float, optional
        MAD threshold for outlier detection (by default 3.5).
    consensus_threshold : float, optional
        Fraction of methods that must agree for consensus (by default 0.5).

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
        - outlier_indices: Indices of consensus outliers
        - outlier_values: Values of consensus outliers
        - method_results: Per-method outlier detection results
        - consensus_scores: Fraction of methods flagging each point

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or parameters have invalid values.

    Examples
    --------
    >>> data = [1, 2, 3, 4, 5, 100]
    >>> result = detect_outliers(data)
    >>> result['outlier_indices']
    array([5])

    >>> result = detect_outliers(data, methods=["zscore", "iqr"])
    >>> len(result['method_results'])
    2

    Notes
    -----
    Uses multiple complementary methods:
    - Z-score: Assumes normal distribution
    - IQR: Non-parametric, robust to non-normal data
    - MAD: Median-based, very robust to outliers
    - Isolation Forest: ML-based, detects multivariate outliers

    Complexity
    ----------
    Time: O(n log n), Space: O(n)
    """
    # Input validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if methods is not None and not isinstance(methods, list):
        raise TypeError(f"methods must be a list or None, got {type(methods).__name__}")
    if not isinstance(zscore_threshold, (int, float)):
        raise TypeError(f"zscore_threshold must be a number, got {type(zscore_threshold).__name__}")
    if not isinstance(iqr_multiplier, (int, float)):
        raise TypeError(f"iqr_multiplier must be a number, got {type(iqr_multiplier).__name__}")
    if not isinstance(mad_threshold, (int, float)):
        raise TypeError(f"mad_threshold must be a number, got {type(mad_threshold).__name__}")
    if not isinstance(consensus_threshold, (int, float)):
        raise TypeError(f"consensus_threshold must be a number, got {type(consensus_threshold).__name__}")

    data_array = np.asarray(data, dtype=float)

    if data_array.size == 0:
        raise ValueError("data cannot be empty")
    if zscore_threshold <= 0:
        raise ValueError(f"zscore_threshold must be positive, got {zscore_threshold}")
    if iqr_multiplier <= 0:
        raise ValueError(f"iqr_multiplier must be positive, got {iqr_multiplier}")
    if mad_threshold <= 0:
        raise ValueError(f"mad_threshold must be positive, got {mad_threshold}")
    if not 0 < consensus_threshold <= 1:
        raise ValueError(f"consensus_threshold must be in (0, 1], got {consensus_threshold}")

    if methods is None:
        methods = ["zscore", "iqr", "mad"]

    valid_methods = {"zscore", "iqr", "mad", "isolation"}
    for method in methods:
        if method not in valid_methods:
            raise ValueError(f"Invalid method '{method}'. Valid methods: {valid_methods}")

    method_results: dict[str, NDArray[np.bool_]] = {}

    # Z-score method
    if "zscore" in methods:
        z_scores = np.abs(stats.zscore(data_array, nan_policy="omit"))
        method_results["zscore"] = z_scores > zscore_threshold

    # IQR method
    if "iqr" in methods:
        q1, q3 = np.percentile(data_array, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - iqr_multiplier * iqr
        upper_bound = q3 + iqr_multiplier * iqr
        method_results["iqr"] = (data_array < lower_bound) | (data_array > upper_bound)

    # MAD method
    if "mad" in methods:
        median = np.median(data_array)
        mad = np.median(np.abs(data_array - median))
        if mad == 0:
            # Avoid division by zero
            mad = 1e-10
        modified_z_scores = 0.6745 * (data_array - median) / mad
        method_results["mad"] = np.abs(modified_z_scores) > mad_threshold

    # Isolation Forest method
    if "isolation" in methods:
        try:
            from sklearn.ensemble import IsolationForest

            iso_forest = IsolationForest(contamination="auto", random_state=42)
            predictions = iso_forest.fit_predict(data_array.reshape(-1, 1))
            method_results["isolation"] = predictions == -1
        except ImportError:
            # Skip isolation forest if sklearn not available
            pass

    # Calculate consensus
    n_methods = len(method_results)
    consensus_votes = np.zeros(len(data_array), dtype=int)

    for outlier_mask in method_results.values():
        consensus_votes += outlier_mask.astype(int)

    consensus_scores = consensus_votes / n_methods
    outlier_mask = consensus_scores >= consensus_threshold

    outlier_indices = np.where(outlier_mask)[0]
    outlier_values = data_array[outlier_mask]

    return {
        "outlier_indices": outlier_indices,
        "outlier_values": outlier_values,
        "method_results": method_results,
        "consensus_scores": consensus_scores,
    }


__all__ = ["detect_outliers"]
