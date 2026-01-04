"""
Data-to-visualization transformers for preparing data for plotting.

This module provides utilities for transforming raw data into formats suitable
for visualization, including binning, aggregation, normalization, and pivoting.
"""

import logging
from typing import Any, Literal

import numpy as np

logger = logging.getLogger(__name__)


def normalize_data(
    data: list[float] | np.ndarray,
    method: Literal['minmax', 'zscore', 'robust'] = 'minmax',
) -> np.ndarray:
    """
    Normalize data for visualization.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Data to normalize.
    method : Literal['minmax', 'zscore', 'robust'], optional
        Normalization method (by default 'minmax').
        - 'minmax': Scale to [0, 1] range
        - 'zscore': Standardize to mean=0, std=1
        - 'robust': Scale using median and IQR (robust to outliers)

    Returns
    -------
    np.ndarray
        Normalized data.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or method is invalid.

    Examples
    --------
    >>> data = [1, 2, 3, 4, 5]
    >>> normalized = normalize_data(data, method='minmax')
    >>> normalized.min(), normalized.max()
    (0.0, 1.0)

    >>> data = np.random.randn(100)
    >>> normalized = normalize_data(data, method='zscore')
    >>> abs(normalized.mean()) < 0.01  # Close to 0
    True

    Notes
    -----
    Normalization methods:
    - minmax: (x - min) / (max - min)
    - zscore: (x - mean) / std
    - robust: (x - median) / IQR

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is data size
    """
    # Type validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}")

    # Convert to numpy array
    data = np.asarray(data, dtype=float)

    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")

    valid_methods = ['minmax', 'zscore', 'robust']
    if method not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}, got '{method}'")

    # Apply normalization
    if method == 'minmax':
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max == data_min:
            logger.warning("All values are identical, returning zeros")
            return np.zeros_like(data)
        normalized = (data - data_min) / (data_max - data_min)

    elif method == 'zscore':
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            logger.warning("Standard deviation is zero, returning zeros")
            return np.zeros_like(data)
        normalized = (data - mean) / std

    else:  # robust
        median = np.median(data)
        q75 = np.percentile(data, 75)
        q25 = np.percentile(data, 25)
        iqr = q75 - q25
        if iqr == 0:
            logger.warning("IQR is zero, returning zeros")
            return np.zeros_like(data)
        normalized = (data - median) / iqr

    logger.debug(f"Normalized {len(data)} values using method '{method}'")
    return normalized


def bin_data(
    data: list[float] | np.ndarray,
    n_bins: int = 10,
    method: Literal['equal_width', 'equal_count', 'quantile'] = 'equal_width',
) -> tuple[np.ndarray, np.ndarray]:
    """
    Bin continuous data into discrete bins for visualization.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Data to bin.
    n_bins : int, optional
        Number of bins (by default 10).
    method : Literal['equal_width', 'equal_count', 'quantile'], optional
        Binning method (by default 'equal_width').
        - 'equal_width': Bins of equal width
        - 'equal_count': Bins with equal number of observations
        - 'quantile': Bins based on quantiles

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Tuple of (bin_assignments, bin_edges) where bin_assignments is an array
        of bin indices for each data point, and bin_edges defines the bin boundaries.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or parameters are invalid.

    Examples
    --------
    >>> data = np.random.randn(1000)
    >>> bin_assignments, bin_edges = bin_data(data, n_bins=5)
    >>> len(bin_edges)
    6  # n_bins + 1 edges

    >>> # Equal count binning
    >>> assignments, edges = bin_data(data, n_bins=4, method='equal_count')
    >>> # Each bin has approximately equal number of observations

    Notes
    -----
    Binning is useful for histograms, heatmaps, and reducing visualization complexity.

    Complexity
    ----------
    Time: O(n*log(n)) for sorting-based methods, Space: O(n)
    """
    # Type validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if not isinstance(n_bins, int):
        raise TypeError(f"n_bins must be an integer, got {type(n_bins).__name__}")
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}")

    # Convert to numpy array
    data = np.asarray(data, dtype=float)

    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    if n_bins <= 0:
        raise ValueError(f"n_bins must be positive, got {n_bins}")

    valid_methods = ['equal_width', 'equal_count', 'quantile']
    if method not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}, got '{method}'")

    # Apply binning
    if method == 'equal_width':
        bin_edges = np.linspace(np.min(data), np.max(data), n_bins + 1)
        bin_assignments = np.digitize(data, bin_edges[1:-1])

    elif method == 'equal_count':
        # Sort data and divide into equal-sized groups
        sorted_indices = np.argsort(data)
        bin_assignments = np.zeros(len(data), dtype=int)
        bin_size = len(data) / n_bins

        for i in range(n_bins):
            start_idx = int(i * bin_size)
            end_idx = int((i + 1) * bin_size) if i < n_bins - 1 else len(data)
            bin_assignments[sorted_indices[start_idx:end_idx]] = i

        # Create bin edges based on assignments
        bin_edges = np.zeros(n_bins + 1)
        bin_edges[0] = np.min(data)
        bin_edges[-1] = np.max(data)
        for i in range(1, n_bins):
            # Find the boundary between bins
            in_bin_i_minus_1 = data[bin_assignments == i - 1]
            in_bin_i = data[bin_assignments == i]
            bin_edges[i] = (np.max(in_bin_i_minus_1) + np.min(in_bin_i)) / 2

    else:  # quantile
        quantiles = np.linspace(0, 100, n_bins + 1)
        bin_edges = np.percentile(data, quantiles)
        bin_assignments = np.digitize(data, bin_edges[1:-1])

    logger.debug(f"Binned {len(data)} values into {n_bins} bins using method '{method}'")
    return bin_assignments, bin_edges


def aggregate_by_group(
    data: list[float] | np.ndarray,
    groups: list[str] | list[int] | np.ndarray,
    agg_func: Literal['mean', 'sum', 'median', 'min', 'max', 'std', 'count'] = 'mean',
) -> tuple[list[Any], list[float]]:
    """
    Aggregate data by groups for visualization.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Data values to aggregate.
    groups : list[str] | list[int] | np.ndarray
        Group labels for each data point.
    agg_func : Literal['mean', 'sum', 'median', 'min', 'max', 'std', 'count'], optional
        Aggregation function (by default 'mean').

    Returns
    -------
    tuple[list[Any], list[float]]
        Tuple of (unique_groups, aggregated_values) where unique_groups contains
        the unique group labels and aggregated_values contains the aggregated
        values for each group.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data and groups have different lengths or are empty.

    Examples
    --------
    >>> data = [10, 20, 30, 40, 50, 60]
    >>> groups = ['A', 'B', 'A', 'B', 'A', 'B']
    >>> unique_groups, agg_values = aggregate_by_group(data, groups, 'mean')
    >>> dict(zip(unique_groups, agg_values))
    {'A': 30.0, 'B': 40.0}

    >>> # Count observations per group
    >>> _, counts = aggregate_by_group(data, groups, 'count')
    >>> counts
    [3, 3]

    Notes
    -----
    Useful for creating bar plots, box plots, and summary visualizations
    of grouped data.

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is data size
    """
    # Type validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if not isinstance(groups, (list, np.ndarray)):
        raise TypeError(f"groups must be a list or numpy array, got {type(groups).__name__}")
    if not isinstance(agg_func, str):
        raise TypeError(f"agg_func must be a string, got {type(agg_func).__name__}")

    # Convert to numpy arrays
    data = np.asarray(data, dtype=float)
    groups = np.asarray(groups)

    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    if len(groups) == 0:
        raise ValueError("groups cannot be empty")
    if len(data) != len(groups):
        raise ValueError(f"data length ({len(data)}) must match groups length ({len(groups)})")

    valid_funcs = ['mean', 'sum', 'median', 'min', 'max', 'std', 'count']
    if agg_func not in valid_funcs:
        raise ValueError(f"agg_func must be one of {valid_funcs}, got '{agg_func}'")

    # Get unique groups while preserving order
    unique_groups = []
    seen = set()
    for group in groups:
        if group not in seen:
            unique_groups.append(group)
            seen.add(group)

    # Aggregate by group
    aggregated_values = []
    for group in unique_groups:
        group_mask = groups == group
        group_data = data[group_mask]

        if agg_func == 'mean':
            value = float(np.mean(group_data))
        elif agg_func == 'sum':
            value = float(np.sum(group_data))
        elif agg_func == 'median':
            value = float(np.median(group_data))
        elif agg_func == 'min':
            value = float(np.min(group_data))
        elif agg_func == 'max':
            value = float(np.max(group_data))
        elif agg_func == 'std':
            value = float(np.std(group_data))
        else:  # count
            value = float(len(group_data))

        aggregated_values.append(value)

    logger.debug(f"Aggregated {len(data)} values into {len(unique_groups)} groups using '{agg_func}'")
    return unique_groups, aggregated_values


def pivot_for_heatmap(
    data: list[tuple[Any, Any, float]],
) -> tuple[list[Any], list[Any], np.ndarray]:
    """
    Pivot data into a 2D matrix suitable for heatmap visualization.

    Parameters
    ----------
    data : list[tuple[Any, Any, float]]
        List of (row_label, col_label, value) tuples.

    Returns
    -------
    tuple[list[Any], list[Any], np.ndarray]
        Tuple of (row_labels, col_labels, matrix) where matrix is a 2D array
        with dimensions (len(row_labels), len(col_labels)).

    Raises
    ------
    TypeError
        If data is not a list of tuples.
    ValueError
        If data is empty or tuples have wrong format.

    Examples
    --------
    >>> data = [
    ...     ('A', 'X', 10),
    ...     ('A', 'Y', 20),
    ...     ('B', 'X', 30),
    ...     ('B', 'Y', 40)
    ... ]
    >>> rows, cols, matrix = pivot_for_heatmap(data)
    >>> rows
    ['A', 'B']
    >>> cols
    ['X', 'Y']
    >>> matrix.shape
    (2, 2)

    Notes
    -----
    Missing combinations are filled with NaN values. This is useful for
    creating heatmaps, confusion matrices, and correlation plots.

    Complexity
    ----------
    Time: O(n), Space: O(n) where n is number of data points
    """
    # Type validation
    if not isinstance(data, list):
        raise TypeError(f"data must be a list, got {type(data).__name__}")

    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")

    # Validate tuple structure
    for i, item in enumerate(data):
        if not isinstance(item, tuple):
            raise TypeError(f"data item {i} must be a tuple, got {type(item).__name__}")
        if len(item) != 3:
            raise ValueError(f"data item {i} must have 3 elements (row, col, value), got {len(item)}")

    # Extract unique row and column labels
    row_labels = []
    col_labels = []
    row_set = set()
    col_set = set()

    for row, col, _ in data:
        if row not in row_set:
            row_labels.append(row)
            row_set.add(row)
        if col not in col_set:
            col_labels.append(col)
            col_set.add(col)

    # Create matrix
    matrix = np.full((len(row_labels), len(col_labels)), np.nan)

    # Create lookup dictionaries
    row_idx = {label: i for i, label in enumerate(row_labels)}
    col_idx = {label: i for i, label in enumerate(col_labels)}

    # Fill matrix
    for row, col, value in data:
        i = row_idx[row]
        j = col_idx[col]
        matrix[i, j] = float(value)

    logger.debug(f"Pivoted {len(data)} data points into {matrix.shape} matrix")
    return row_labels, col_labels, matrix


def smooth_timeseries(
    data: list[float] | np.ndarray,
    window_size: int = 5,
    method: Literal['moving_average', 'exponential', 'gaussian'] = 'moving_average',
) -> np.ndarray:
    """
    Smooth timeseries data for cleaner visualization.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Timeseries data to smooth.
    window_size : int, optional
        Size of the smoothing window (by default 5).
    method : Literal['moving_average', 'exponential', 'gaussian'], optional
        Smoothing method (by default 'moving_average').

    Returns
    -------
    np.ndarray
        Smoothed data.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or parameters are invalid.

    Examples
    --------
    >>> noisy_data = [1, 5, 2, 8, 3, 9, 4, 10]
    >>> smoothed = smooth_timeseries(noisy_data, window_size=3)
    >>> len(smoothed)
    8

    >>> # Exponential smoothing
    >>> smoothed = smooth_timeseries(noisy_data, method='exponential')
    >>> # Recent values have more influence

    Notes
    -----
    Smoothing methods:
    - moving_average: Simple moving average
    - exponential: Exponential weighted moving average
    - gaussian: Gaussian-weighted moving average

    Complexity
    ----------
    Time: O(n*w) where w is window_size, Space: O(n)
    """
    # Type validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if not isinstance(window_size, int):
        raise TypeError(f"window_size must be an integer, got {type(window_size).__name__}")
    if not isinstance(method, str):
        raise TypeError(f"method must be a string, got {type(method).__name__}")

    # Convert to numpy array
    data = np.asarray(data, dtype=float)

    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    if window_size <= 0:
        raise ValueError(f"window_size must be positive, got {window_size}")
    if window_size > len(data):
        raise ValueError(f"window_size ({window_size}) cannot exceed data length ({len(data)})")

    valid_methods = ['moving_average', 'exponential', 'gaussian']
    if method not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}, got '{method}'")

    # Apply smoothing
    if method == 'moving_average':
        # Simple moving average
        smoothed = np.convolve(data, np.ones(window_size) / window_size, mode='same')

    elif method == 'exponential':
        # Exponential weighted moving average
        alpha = 2.0 / (window_size + 1)
        smoothed = np.zeros_like(data)
        smoothed[0] = data[0]
        for i in range(1, len(data)):
            smoothed[i] = alpha * data[i] + (1 - alpha) * smoothed[i - 1]

    else:  # gaussian
        # Gaussian-weighted moving average
        sigma = window_size / 3.0
        x = np.arange(-window_size // 2 + 1, window_size // 2 + 1)
        kernel = np.exp(-x**2 / (2 * sigma**2))
        kernel = kernel / kernel.sum()
        smoothed = np.convolve(data, kernel, mode='same')

    logger.debug(f"Smoothed {len(data)} values using method '{method}' with window_size={window_size}")
    return smoothed


def calculate_moving_statistics(
    data: list[float] | np.ndarray,
    window_size: int = 10,
    statistic: Literal['mean', 'median', 'std', 'min', 'max'] = 'mean',
) -> np.ndarray:
    """
    Calculate moving statistics for timeseries visualization.

    Parameters
    ----------
    data : list[float] | np.ndarray
        Timeseries data.
    window_size : int, optional
        Size of the moving window (by default 10).
    statistic : Literal['mean', 'median', 'std', 'min', 'max'], optional
        Statistic to calculate (by default 'mean').

    Returns
    -------
    np.ndarray
        Array of moving statistics.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If data is empty or parameters are invalid.

    Examples
    --------
    >>> data = np.random.randn(100)
    >>> moving_mean = calculate_moving_statistics(data, window_size=10, statistic='mean')
    >>> len(moving_mean)
    100

    >>> moving_std = calculate_moving_statistics(data, window_size=10, statistic='std')
    >>> # Shows volatility over time

    Notes
    -----
    Useful for visualizing trends, volatility, and ranges in timeseries data.
    Edge values use smaller windows to maintain array length.

    Complexity
    ----------
    Time: O(n*w) where w is window_size, Space: O(n)
    """
    # Type validation
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError(f"data must be a list or numpy array, got {type(data).__name__}")
    if not isinstance(window_size, int):
        raise TypeError(f"window_size must be an integer, got {type(window_size).__name__}")
    if not isinstance(statistic, str):
        raise TypeError(f"statistic must be a string, got {type(statistic).__name__}")

    # Convert to numpy array
    data = np.asarray(data, dtype=float)

    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    if window_size <= 0:
        raise ValueError(f"window_size must be positive, got {window_size}")

    valid_statistics = ['mean', 'median', 'std', 'min', 'max']
    if statistic not in valid_statistics:
        raise ValueError(f"statistic must be one of {valid_statistics}, got '{statistic}'")

    # Calculate moving statistic
    result = np.zeros(len(data))

    for i in range(len(data)):
        # Determine window boundaries
        start = max(0, i - window_size // 2)
        end = min(len(data), i + window_size // 2 + 1)
        window = data[start:end]

        # Calculate statistic
        if statistic == 'mean':
            result[i] = np.mean(window)
        elif statistic == 'median':
            result[i] = np.median(window)
        elif statistic == 'std':
            result[i] = np.std(window)
        elif statistic == 'min':
            result[i] = np.min(window)
        else:  # max
            result[i] = np.max(window)

    logger.debug(f"Calculated moving {statistic} for {len(data)} values with window_size={window_size}")
    return result


__all__ = [
    'normalize_data',
    'bin_data',
    'aggregate_by_group',
    'pivot_for_heatmap',
    'smooth_timeseries',
    'calculate_moving_statistics',
]
