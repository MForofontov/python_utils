"""Perform correlation analysis with multiple statistical tests and confidence intervals."""

from typing import Union, List, Dict, Tuple
import math


def correlation_analysis(x: list[Union[int, float]], 
                        y: list[Union[int, float]], 
                        method: str = 'pearson',
                        confidence_level: float = 0.95) -> Dict[str, Union[float, Tuple[float, float], str]]:
    """
    Perform comprehensive correlation analysis with statistical significance testing.

    Calculates correlation coefficients, confidence intervals, and hypothesis tests.
    Supports Pearson, Spearman, and Kendall correlation methods.

    Parameters
    ----------
    x : list[int | float]
        First variable values.
    y : list[int | float]
        Second variable values (must be same length as x).
    method : str, optional
        Correlation method: 'pearson', 'spearman', or 'kendall'. Default 'pearson'.
    confidence_level : float, optional
        Confidence level for intervals (0 < confidence_level < 1). Default 0.95.

    Returns
    -------
    dict[str, Union[float, Tuple[float, float], str]]
        Dictionary containing:
        - 'correlation': Correlation coefficient
        - 'p_value': Two-tailed p-value for significance test
        - 'confidence_interval': Tuple of (lower, upper) bounds
        - 'sample_size': Number of data points
        - 'degrees_freedom': Degrees of freedom
        - 'test_statistic': Test statistic value
        - 'interpretation': Textual interpretation of strength
        - 'is_significant': Boolean indicating statistical significance

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If data validation fails or method is invalid.

    Examples
    --------
    >>> result = correlation_analysis([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    >>> abs(result['correlation'] - 1.0) < 1e-10
    True
    >>> result['is_significant']
    True
    """
    # Input validation
    if not isinstance(x, list):
        raise TypeError("x must be a list")
    if not isinstance(y, list):
        raise TypeError("y must be a list")
    if not isinstance(method, str):
        raise TypeError("method must be a string")
    if not isinstance(confidence_level, (int, float)):
        raise TypeError("confidence_level must be numeric")
    
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    if len(x) < 3:
        raise ValueError("need at least 3 data points for correlation analysis")
    
    if not all(isinstance(val, (int, float)) for val in x):
        raise TypeError("all values in x must be numeric")
    if not all(isinstance(val, (int, float)) for val in y):
        raise TypeError("all values in y must be numeric")
    
    valid_methods = ['pearson', 'spearman', 'kendall']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1")
    
    method = method.lower()
    n = len(x)
    
    # Calculate correlation coefficient based on method
    if method == 'pearson':
        correlation = _pearson_correlation(x, y)
        test_stat = _pearson_test_statistic(correlation, n)
        df = n - 2
        p_value = _t_test_p_value(test_stat, df)
        conf_interval = _pearson_confidence_interval(correlation, n, confidence_level)
        
    elif method == 'spearman':
        correlation = _spearman_correlation(x, y)
        test_stat = _spearman_test_statistic(correlation, n)
        df = n - 2
        p_value = _t_test_p_value(test_stat, df) if n > 30 else _spearman_exact_p_value(correlation, n)
        conf_interval = _spearman_confidence_interval(correlation, n, confidence_level)
        
    elif method == 'kendall':
        correlation = _kendall_correlation(x, y)
        test_stat = _kendall_test_statistic(correlation, n)
        df = float('inf')  # Normal approximation
        p_value = _normal_test_p_value(test_stat)
        conf_interval = _kendall_confidence_interval(correlation, n, confidence_level)
    
    # Interpret correlation strength
    interpretation = _interpret_correlation(correlation)
    
    # Determine statistical significance
    alpha = 1 - confidence_level
    is_significant = p_value < alpha
    
    return {
        'correlation': correlation,
        'p_value': p_value,
        'confidence_interval': conf_interval,
        'sample_size': n,
        'degrees_freedom': df,
        'test_statistic': test_stat,
        'interpretation': interpretation,
        'is_significant': is_significant
    }


def _pearson_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient."""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def _spearman_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Spearman rank correlation coefficient."""
    # Convert to ranks
    x_ranks = _convert_to_ranks(x)
    y_ranks = _convert_to_ranks(y)
    
    # Calculate Pearson correlation of ranks
    return _pearson_correlation(x_ranks, y_ranks)


def _kendall_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Kendall's tau correlation coefficient."""
    n = len(x)
    concordant = 0
    discordant = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            x_diff = x[i] - x[j]
            y_diff = y[i] - y[j]
            
            if x_diff * y_diff > 0:
                concordant += 1
            elif x_diff * y_diff < 0:
                discordant += 1
            # Ties contribute 0
    
    total_pairs = n * (n - 1) // 2
    if total_pairs == 0:
        return 0.0
    
    return (concordant - discordant) / total_pairs


def _convert_to_ranks(data: List[float]) -> List[float]:
    """Convert data to ranks, handling ties with average rank."""
    n = len(data)
    indexed_data = [(data[i], i) for i in range(n)]
    indexed_data.sort()
    
    ranks = [0.0] * n
    i = 0
    
    while i < n:
        j = i
        # Find end of tied group
        while j < n and indexed_data[j][0] == indexed_data[i][0]:
            j += 1
        
        # Calculate average rank for tied group
        avg_rank = (i + j + 1) / 2.0
        
        # Assign average rank to all tied values
        for k in range(i, j):
            original_index = indexed_data[k][1]
            ranks[original_index] = avg_rank
        
        i = j
    
    return ranks


def _pearson_test_statistic(r: float, n: int) -> float:
    """Calculate t-statistic for Pearson correlation."""
    if abs(r) >= 1.0:
        return float('inf') if r > 0 else float('-inf')
    
    return r * math.sqrt((n - 2) / (1 - r ** 2))


def _spearman_test_statistic(r: float, n: int) -> float:
    """Calculate test statistic for Spearman correlation."""
    return _pearson_test_statistic(r, n)  # Same formula for large n


def _kendall_test_statistic(tau: float, n: int) -> float:
    """Calculate z-statistic for Kendall correlation (normal approximation)."""
    variance = 2 * (2 * n + 5) / (9 * n * (n - 1))
    return tau / math.sqrt(variance)


def _t_test_p_value(t: float, df: int) -> float:
    """Calculate two-tailed p-value for t-distribution (approximation)."""
    if math.isinf(t):
        return 0.0
    
    # Simple approximation for t-distribution p-value
    # More accurate methods would require complex mathematical functions
    if df > 30:
        # Use normal approximation for large df
        return 2 * (1 - _standard_normal_cdf(abs(t)))
    else:
        # Rough approximation for small df
        return 2 * (1 - _standard_normal_cdf(abs(t) * math.sqrt(df / (df + t**2))))


def _normal_test_p_value(z: float) -> float:
    """Calculate two-tailed p-value for standard normal distribution."""
    return 2 * (1 - _standard_normal_cdf(abs(z)))


def _standard_normal_cdf(z: float) -> float:
    """Approximate cumulative distribution function of standard normal."""
    # Approximation using error function
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _pearson_confidence_interval(r: float, n: int, confidence: float) -> Tuple[float, float]:
    """Calculate confidence interval for Pearson correlation using Fisher transformation."""
    if n <= 3:
        return (-1.0, 1.0)
    
    # Fisher z-transformation
    z_r = 0.5 * math.log((1 + r) / (1 - r)) if abs(r) < 0.999 else (10.0 if r > 0 else -10.0)
    
    # Standard error of z
    se_z = 1 / math.sqrt(n - 3)
    
    # Critical value (approximate)
    alpha = 1 - confidence
    z_critical = _inverse_normal_cdf(1 - alpha / 2)
    
    # Confidence interval in z-space
    z_lower = z_r - z_critical * se_z
    z_upper = z_r + z_critical * se_z
    
    # Transform back to correlation space
    r_lower = (math.exp(2 * z_lower) - 1) / (math.exp(2 * z_lower) + 1)
    r_upper = (math.exp(2 * z_upper) - 1) / (math.exp(2 * z_upper) + 1)
    
    return (max(r_lower, -1.0), min(r_upper, 1.0))


def _spearman_confidence_interval(r: float, n: int, confidence: float) -> Tuple[float, float]:
    """Approximate confidence interval for Spearman correlation."""
    # Use same method as Pearson for large n
    return _pearson_confidence_interval(r, n, confidence)


def _kendall_confidence_interval(tau: float, n: int, confidence: float) -> Tuple[float, float]:
    """Approximate confidence interval for Kendall correlation."""
    if n < 10:
        return (-1.0, 1.0)
    
    # Standard error approximation
    se_tau = math.sqrt(2 * (2 * n + 5) / (9 * n * (n - 1)))
    
    alpha = 1 - confidence
    z_critical = _inverse_normal_cdf(1 - alpha / 2)
    
    margin = z_critical * se_tau
    
    return (max(tau - margin, -1.0), min(tau + margin, 1.0))


def _inverse_normal_cdf(p: float) -> float:
    """Approximate inverse of standard normal CDF."""
    # Beasley-Springer-Moro approximation
    if p <= 0.5:
        return -_inverse_normal_cdf(1 - p)
    
    t = math.sqrt(-2 * math.log(1 - p))
    
    # Coefficients for approximation
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    
    return t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)


def _spearman_exact_p_value(r: float, n: int) -> float:
    """Exact p-value for small sample Spearman correlation (simplified)."""
    # This is a simplified approximation
    # Real implementation would require extensive tables or permutation tests
    return _t_test_p_value(_pearson_test_statistic(r, n), n - 2)


def _interpret_correlation(r: float) -> str:
    """Interpret correlation coefficient strength."""
    abs_r = abs(r)
    
    if abs_r < 0.1:
        strength = "negligible"
    elif abs_r < 0.3:
        strength = "weak"
    elif abs_r < 0.5:
        strength = "moderate"
    elif abs_r < 0.7:
        strength = "strong"
    else:
        strength = "very strong"
    
    direction = "positive" if r >= 0 else "negative"
    
    return f"{strength} {direction} correlation"


__all__ = ['correlation_analysis']
