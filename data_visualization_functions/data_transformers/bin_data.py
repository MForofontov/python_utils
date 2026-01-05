"""
Bin continuous data into discrete intervals.
"""

import logging
import numpy as np
from numpy.typing import ArrayLike

logger = logging.getLogger(__name__)


def bin_data(
    data: ArrayLike,
    bins: int | ArrayLike = 10,
    labels: list[str] | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Bin continuous data into discrete intervals.

    Parameters
    ----------
    data : ArrayLike
        Input data to bin.
    bins : int | ArrayLike, optional
        Number of equal-width bins or array of bin edges (by default 10).
    labels : list[str] | None, optional
        Labels for bins (by default None, uses bin indices).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Tuple of (binned_indices, bin_edges):
        - binned_indices: Array of bin indices for each data point
        - bin_edges: Array of bin edge values

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If bins is invalid or labels length mismatches.

    Examples
    --------
    >>> data = [1.2, 2.5, 3.8, 5.1, 7.3]
    >>> indices, edges = bin_data(data, bins=3)
    >>> len(indices)
    5

    >>> indices, edges = bin_data(data, bins=[0, 3, 6, 10])
    >>> len(edges)
    4

    Notes
    -----
    Uses numpy.digitize for binning. Bin indices are 0-based.
    Values outside bin edges are assigned to nearest bin.

    Complexity
    ----------
    Time: O(n log m) where m is number of bins, Space: O(n)
    """
    # Type validation
    if labels is not None and not isinstance(labels, list):
        raise TypeError(f"labels must be a list or None, got {type(labels).__name__}")

    # Convert to numpy array
    try:
        data_array = np.asarray(data, dtype=float)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Cannot convert data to numeric array: {e}") from e

    if data_array.size == 0:
        raise ValueError("data cannot be empty")

    # Handle bins parameter
    if isinstance(bins, int):
        if bins < 1:
            raise ValueError(f"bins must be positive, got {bins}")

        # Create equal-width bins
        data_min = np.min(data_array)
        data_max = np.max(data_array)
        bin_edges = np.linspace(data_min, data_max, bins + 1)

    else:
        try:
            bin_edges = np.asarray(bins, dtype=float)
        except (ValueError, TypeError) as e:
            raise TypeError(f"bins must be int or array-like: {e}") from e

        if bin_edges.size < 2:
            raise ValueError("bin_edges must have at least 2 elements")

        if not np.all(bin_edges[:-1] < bin_edges[1:]):
            raise ValueError("bin_edges must be strictly increasing")

    # Validate labels
    n_bins = len(bin_edges) - 1
    if labels is not None and len(labels) != n_bins:
        raise ValueError(
            f"labels length ({len(labels)}) must match number of bins ({n_bins})"
        )

    logger.debug(f"Binning {data_array.size} values into {n_bins} bins")

    # Digitize returns 1-based indices, convert to 0-based
    binned_indices = np.digitize(data_array, bin_edges, right=False) - 1

    # Clamp to valid range [0, n_bins-1]
    binned_indices = np.clip(binned_indices, 0, n_bins - 1)

    logger.debug(f"Binned data: min_bin={binned_indices.min()}, max_bin={binned_indices.max()}")
    return binned_indices, bin_edges


__all__ = ['bin_data']
