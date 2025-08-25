"""
Outlier detection using various statistical methods.

This module provides multiple methods for detecting outliers in datasets,
including IQR, z-score, modified z-score, and isolation methods.
"""

import math
from typing import List, Union, Dict, Any, Tuple


def outlier_detection(values: List[Union[int, float]], 
                     method: str = 'iqr', 
                     threshold: float = None) -> Dict[str, Any]:
    """
    Detect outliers using various statistical methods.
    
    Supports multiple outlier detection methods with customizable thresholds.
    
    Args:
        values: List of numeric values to analyze
        method: Detection method. Options:
               - 'iqr': Interquartile Range method (default)
               - 'zscore': Z-score method (standard score)
               - 'modified_zscore': Modified Z-score using median absolute deviation
               - 'isolation': Isolation-based outlier detection (simplified)
               - 'grubbs': Grubbs' test for outliers (single outlier)
        threshold: Threshold value for outlier detection:
                  - IQR: multiplier for IQR (default: 1.5)
                  - Z-score: standard deviations (default: 3.0)
                  - Modified Z-score: MAD multiplier (default: 3.5)
                  - Isolation: isolation score threshold (default: 0.6)
                  - Grubbs: significance level (default: 0.05)
    
    Returns:
        Dict containing:
        - 'outliers': List of outlier values
        - 'outlier_indices': List of indices of outliers
        - 'inliers': List of non-outlier values
        - 'outlier_scores': List of outlier scores/distances
        - 'method_used': Method used for detection
        - 'threshold_used': Threshold value used
        - 'summary': Summary statistics
        
    Raises:
        TypeError: If inputs are not proper types
        ValueError: If data validation fails or method is unknown
        
    Examples:
        >>> result = outlier_detection([1, 2, 3, 4, 5, 100])
        >>> 100 in result['outliers']
        True
    """
    # Input validation
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    
    if len(values) < 4:
        raise ValueError("outlier detection requires at least 4 values")
    
    # Validate numeric types
    for i, val in enumerate(values):
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            raise TypeError("all values must be numeric")
    
    # Validate method
    valid_methods = ['iqr', 'zscore', 'modified_zscore', 'isolation', 'grubbs']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    # Set default thresholds
    if threshold is None:
        threshold_defaults = {
            'iqr': 1.5,
            'zscore': 3.0,
            'modified_zscore': 3.5,
            'isolation': 0.6,
            'grubbs': 0.05
        }
        threshold = threshold_defaults[method.lower()]
    
    # Validate threshold
    if not isinstance(threshold, (int, float)) or threshold <= 0:
        raise ValueError("threshold must be positive")
    
    method = method.lower()
    
    # Apply outlier detection method
    if method == 'iqr':
        result = _iqr_outlier_detection(values, threshold)
    elif method == 'zscore':
        result = _zscore_outlier_detection(values, threshold)
    elif method == 'modified_zscore':
        result = _modified_zscore_outlier_detection(values, threshold)
    elif method == 'isolation':
        result = _isolation_outlier_detection(values, threshold)
    elif method == 'grubbs':
        result = _grubbs_outlier_detection(values, threshold)
    
    # Add metadata
    result['method_used'] = method
    result['threshold_used'] = threshold
    result['summary'] = _calculate_summary_stats(values)
    
    return result


def _iqr_outlier_detection(values: List[Union[int, float]], multiplier: float) -> Dict[str, Any]:
    """Detect outliers using Interquartile Range method."""
    n = len(values)
    sorted_values = sorted(values)
    
    # Calculate quartiles
    q1_idx = (n - 1) * 0.25
    q3_idx = (n - 1) * 0.75
    
    if q1_idx == int(q1_idx):
        q1 = sorted_values[int(q1_idx)]
    else:
        lower_idx = int(q1_idx)
        upper_idx = lower_idx + 1
        weight = q1_idx - lower_idx
        q1 = sorted_values[lower_idx] * (1 - weight) + sorted_values[upper_idx] * weight
    
    if q3_idx == int(q3_idx):
        q3 = sorted_values[int(q3_idx)]
    else:
        lower_idx = int(q3_idx)
        upper_idx = lower_idx + 1
        weight = q3_idx - lower_idx
        q3 = sorted_values[lower_idx] * (1 - weight) + sorted_values[upper_idx] * weight
    
    # Calculate IQR and bounds
    iqr = q3 - q1
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr
    
    # Identify outliers
    outliers = []
    outlier_indices = []
    inliers = []
    outlier_scores = []
    
    for i, value in enumerate(values):
        if value < lower_bound or value > upper_bound:
            outliers.append(value)
            outlier_indices.append(i)
            # Score is distance from nearest bound
            score = min(abs(value - lower_bound), abs(value - upper_bound)) / iqr if iqr > 0 else 0
            outlier_scores.append(score)
        else:
            inliers.append(value)
            outlier_scores.append(0.0)
    
    return {
        'outliers': outliers,
        'outlier_indices': outlier_indices,
        'inliers': inliers,
        'outlier_scores': outlier_scores
    }


def _zscore_outlier_detection(values: List[Union[int, float]], threshold: float) -> Dict[str, Any]:
    """Detect outliers using Z-score method."""
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    
    if variance == 0:
        # All values are identical
        return {
            'outliers': [],
            'outlier_indices': [],
            'inliers': values.copy(),
            'outlier_scores': [0.0] * len(values)
        }
    
    std_dev = math.sqrt(variance)
    
    outliers = []
    outlier_indices = []
    inliers = []
    outlier_scores = []
    
    for i, value in enumerate(values):
        z_score = abs(value - mean) / std_dev
        outlier_scores.append(z_score)
        
        if z_score > threshold:
            outliers.append(value)
            outlier_indices.append(i)
        else:
            inliers.append(value)
    
    return {
        'outliers': outliers,
        'outlier_indices': outlier_indices,
        'inliers': inliers,
        'outlier_scores': outlier_scores
    }


def _modified_zscore_outlier_detection(values: List[Union[int, float]], threshold: float) -> Dict[str, Any]:
    """Detect outliers using Modified Z-score with Median Absolute Deviation."""
    n = len(values)
    sorted_values = sorted(values)
    
    # Calculate median
    if n % 2 == 0:
        median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        median = sorted_values[n//2]
    
    # Calculate Median Absolute Deviation (MAD)
    absolute_deviations = [abs(x - median) for x in values]
    sorted_deviations = sorted(absolute_deviations)
    
    if len(sorted_deviations) % 2 == 0:
        mad = (sorted_deviations[len(sorted_deviations)//2 - 1] + sorted_deviations[len(sorted_deviations)//2]) / 2
    else:
        mad = sorted_deviations[len(sorted_deviations)//2]
    
    if mad == 0:
        # All values are identical to median
        return {
            'outliers': [],
            'outlier_indices': [],
            'inliers': values.copy(),
            'outlier_scores': [0.0] * len(values)
        }
    
    # Calculate modified Z-scores
    outliers = []
    outlier_indices = []
    inliers = []
    outlier_scores = []
    
    for i, value in enumerate(values):
        modified_z_score = 0.6745 * (value - median) / mad
        abs_modified_z = abs(modified_z_score)
        outlier_scores.append(abs_modified_z)
        
        if abs_modified_z > threshold:
            outliers.append(value)
            outlier_indices.append(i)
        else:
            inliers.append(value)
    
    return {
        'outliers': outliers,
        'outlier_indices': outlier_indices,
        'inliers': inliers,
        'outlier_scores': outlier_scores
    }


def _isolation_outlier_detection(values: List[Union[int, float]], threshold: float) -> Dict[str, Any]:
    """Simplified isolation-based outlier detection."""
    # This is a simplified version of isolation forest concept
    n = len(values)
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    if range_val == 0:
        # All values are identical
        return {
            'outliers': [],
            'outlier_indices': [],
            'inliers': values.copy(),
            'outlier_scores': [0.0] * len(values)
        }
    
    outliers = []
    outlier_indices = []
    inliers = []
    outlier_scores = []
    
    for i, value in enumerate(values):
        # Simple isolation score based on distance from center and density
        center = (min_val + max_val) / 2
        distance_from_center = abs(value - center) / range_val
        
        # Count nearby values (density estimation)
        nearby_count = 0
        for other_val in values:
            if abs(value - other_val) <= range_val * 0.1:
                nearby_count += 1
        
        density_score = 1.0 / nearby_count if nearby_count > 0 else 1.0
        isolation_score = distance_from_center * density_score
        outlier_scores.append(isolation_score)
        
        if isolation_score > threshold:
            outliers.append(value)
            outlier_indices.append(i)
        else:
            inliers.append(value)
    
    return {
        'outliers': outliers,
        'outlier_indices': outlier_indices,
        'inliers': inliers,
        'outlier_scores': outlier_scores
    }


def _grubbs_outlier_detection(values: List[Union[int, float]], alpha: float) -> Dict[str, Any]:
    """Detect single outlier using Grubbs' test."""
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    
    if variance == 0:
        # All values are identical
        return {
            'outliers': [],
            'outlier_indices': [],
            'inliers': values.copy(),
            'outlier_scores': [0.0] * len(values)
        }
    
    std_dev = math.sqrt(variance)
    
    # Calculate Grubbs' test statistic for each value
    max_grubbs = 0
    max_index = 0
    grubbs_scores = []
    
    for i, value in enumerate(values):
        grubbs_stat = abs(value - mean) / std_dev
        grubbs_scores.append(grubbs_stat)
        
        if grubbs_stat > max_grubbs:
            max_grubbs = grubbs_stat
            max_index = i
    
    # Approximate critical value for Grubbs' test
    # This is a simplified approximation
    if alpha == 0.05:
        if n < 10:
            critical_value = 2.5
        elif n < 30:
            critical_value = 3.0
        else:
            critical_value = 3.5
    else:
        critical_value = 3.0  # Default approximation
    
    # Identify outlier
    if max_grubbs > critical_value:
        outliers = [values[max_index]]
        outlier_indices = [max_index]
        inliers = [values[i] for i in range(len(values)) if i != max_index]
    else:
        outliers = []
        outlier_indices = []
        inliers = values.copy()
    
    return {
        'outliers': outliers,
        'outlier_indices': outlier_indices,
        'inliers': inliers,
        'outlier_scores': grubbs_scores
    }


def _calculate_summary_stats(values: List[Union[int, float]]) -> Dict[str, float]:
    """Calculate summary statistics for the dataset."""
    n = len(values)
    sorted_values = sorted(values)
    
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1) if n > 1 else 0
    std_dev = math.sqrt(variance)
    
    # Median
    if n % 2 == 0:
        median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        median = sorted_values[n//2]
    
    return {
        'count': n,
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'min': min(values),
        'max': max(values),
        'range': max(values) - min(values)
    }


__all__ = ['outlier_detection']
