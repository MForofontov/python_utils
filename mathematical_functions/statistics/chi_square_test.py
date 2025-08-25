"""
Chi-square statistical tests with multiple test types.

This module provides chi-square tests for goodness of fit, independence,
and homogeneity using various methods and corrections.
"""

import math
from typing import List, Union, Dict, Any, Optional


def chi_square_test(observed: List[List[Union[int, float]]], 
                   expected: Optional[List[List[Union[int, float]]]] = None,
                   method: str = 'pearson',
                   correction: str = 'none') -> Dict[str, Any]:
    """
    Perform chi-square test with various methods and corrections.
    
    Supports different chi-square test variants and continuity corrections.
    
    Args:
        observed: 2D list of observed frequencies
        expected: 2D list of expected frequencies (optional, calculated if None)
        method: Test method. Options:
               - 'pearson': Standard Pearson chi-square test (default)
               - 'log_likelihood': Log-likelihood ratio test (G-test)
               - 'freeman_tukey': Freeman-Tukey residuals test
               - 'neyman_modified': Neyman's modified chi-square
        correction: Continuity correction. Options:
                   - 'none': No correction (default)
                   - 'yates': Yates' continuity correction (for 2x2 tables)
                   - 'williams': Williams' correction for G-test
    
    Returns:
        Dict containing:
        - 'chi_square': Test statistic value
        - 'p_value': P-value (approximation)
        - 'degrees_of_freedom': Degrees of freedom
        - 'critical_value': Critical value at α=0.05
        - 'is_significant': Boolean indicating significance at α=0.05
        - 'effect_size': Effect size measure (Cramér's V)
        
    Raises:
        TypeError: If inputs are not proper types
        ValueError: If data validation fails or method is unknown
        
    Examples:
        >>> observed = [[10, 20], [30, 40]]
        >>> result = chi_square_test(observed)
        >>> result['degrees_of_freedom']
        1
    """
    # Input validation
    if not isinstance(observed, list):
        raise TypeError("observed must be a list of lists")
    
    if len(observed) == 0:
        raise ValueError("observed table cannot be empty")
    
    if not all(isinstance(row, list) for row in observed):
        raise TypeError("observed must be a list of lists")
    
    # Validate dimensions
    rows = len(observed)
    cols = len(observed[0]) if rows > 0 else 0
    
    if cols == 0:
        raise ValueError("observed table cannot be empty")
    
    if not all(len(row) == cols for row in observed):
        raise ValueError("all rows in observed table must have the same length")
    
    # Validate numeric values and non-negativity
    for i, row in enumerate(observed):
        for j, val in enumerate(row):
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                raise TypeError("all values must be numeric")
            if val < 0:
                raise ValueError("observed frequencies must be non-negative")
    
    # Calculate expected frequencies if not provided
    if expected is None:
        expected = _calculate_expected_frequencies(observed)
    else:
        # Validate expected frequencies
        if not isinstance(expected, list):
            raise TypeError("expected must be a list of lists")
        
        if len(expected) != rows or any(len(row) != cols for row in expected):
            raise ValueError("observed and expected tables must have the same dimensions")
        
        for i, row in enumerate(expected):
            for j, val in enumerate(row):
                if not isinstance(val, (int, float)) or isinstance(val, bool):
                    raise TypeError("all values must be numeric")
                if val <= 0:
                    raise ValueError("expected frequencies must be greater than 0")
    
    # Validate method and correction
    valid_methods = ['pearson', 'log_likelihood', 'freeman_tukey', 'neyman_modified']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    valid_corrections = ['none', 'yates', 'williams']
    if correction.lower() not in valid_corrections:
        raise ValueError(f"correction must be one of {valid_corrections}")
    
    # Calculate degrees of freedom
    df = (rows - 1) * (cols - 1)
    
    # Calculate test statistic based on method
    method = method.lower()
    correction = correction.lower()
    
    if method == 'pearson':
        chi_square = _pearson_chi_square(observed, expected, correction)
    elif method == 'log_likelihood':
        chi_square = _log_likelihood_test(observed, expected, correction)
    elif method == 'freeman_tukey':
        chi_square = _freeman_tukey_test(observed, expected)
    elif method == 'neyman_modified':
        chi_square = _neyman_modified_test(observed, expected)
    
    # Calculate p-value (approximation)
    p_value = _chi_square_p_value(chi_square, df)
    
    # Critical value at α = 0.05
    critical_value = _chi_square_critical_value(df, 0.05)
    
    # Significance test
    is_significant = chi_square > critical_value
    
    # Effect size (Cramér's V)
    total_n = sum(sum(row) for row in observed)
    cramers_v = math.sqrt(chi_square / (total_n * min(rows - 1, cols - 1)))
    
    return {
        'chi_square': chi_square,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'critical_value': critical_value,
        'is_significant': is_significant,
        'effect_size': cramers_v
    }


def _calculate_expected_frequencies(observed: List[List[Union[int, float]]]) -> List[List[float]]:
    """Calculate expected frequencies under independence hypothesis."""
    rows = len(observed)
    cols = len(observed[0])
    
    # Calculate marginal totals
    row_totals = [sum(row) for row in observed]
    col_totals = [sum(observed[i][j] for i in range(rows)) for j in range(cols)]
    total = sum(row_totals)
    
    if total == 0:
        raise ValueError("total frequency cannot be zero")
    
    # Calculate expected frequencies
    expected = []
    for i in range(rows):
        row = []
        for j in range(cols):
            exp_freq = (row_totals[i] * col_totals[j]) / total
            row.append(exp_freq)
        expected.append(row)
    
    return expected


def _pearson_chi_square(observed: List[List[Union[int, float]]], 
                       expected: List[List[float]], 
                       correction: str) -> float:
    """Calculate Pearson chi-square statistic."""
    chi_square = 0.0
    rows, cols = len(observed), len(observed[0])
    
    for i in range(rows):
        for j in range(cols):
            obs = observed[i][j]
            exp = expected[i][j]
            
            if correction == 'yates' and rows == 2 and cols == 2:
                # Yates' continuity correction for 2x2 tables
                diff = abs(obs - exp) - 0.5
                if diff < 0:
                    diff = 0
                chi_square += (diff ** 2) / exp
            else:
                chi_square += ((obs - exp) ** 2) / exp
    
    return chi_square


def _log_likelihood_test(observed: List[List[Union[int, float]]], 
                        expected: List[List[float]], 
                        correction: str) -> float:
    """Calculate log-likelihood ratio test statistic (G-test)."""
    g_statistic = 0.0
    rows, cols = len(observed), len(observed[0])
    
    for i in range(rows):
        for j in range(cols):
            obs = observed[i][j]
            exp = expected[i][j]
            
            if obs > 0:  # Avoid log(0)
                g_statistic += obs * math.log(obs / exp)
    
    g_statistic *= 2
    
    if correction == 'williams':
        # Williams' correction for G-test
        total_n = sum(sum(row) for row in observed)
        df = (rows - 1) * (cols - 1)
        correction_factor = 1 + ((rows * cols + 1) / (6 * total_n * df))
        g_statistic /= correction_factor
    
    return g_statistic


def _freeman_tukey_test(observed: List[List[Union[int, float]]], 
                       expected: List[List[float]]) -> float:
    """Calculate Freeman-Tukey test statistic."""
    ft_statistic = 0.0
    
    for i in range(len(observed)):
        for j in range(len(observed[0])):
            obs = observed[i][j]
            exp = expected[i][j]
            
            # Freeman-Tukey transformation
            ft_residual = math.sqrt(obs) + math.sqrt(obs + 1) - math.sqrt(4 * exp + 1)
            ft_statistic += ft_residual ** 2
    
    return ft_statistic


def _neyman_modified_test(observed: List[List[Union[int, float]]], 
                         expected: List[List[float]]) -> float:
    """Calculate Neyman's modified chi-square statistic."""
    nm_statistic = 0.0
    
    for i in range(len(observed)):
        for j in range(len(observed[0])):
            obs = observed[i][j]
            exp = expected[i][j]
            
            if obs > 0:  # Avoid division by zero
                nm_statistic += ((obs - exp) ** 2) / obs
    
    return nm_statistic


def _chi_square_p_value(chi_square: float, df: int) -> float:
    """Approximate p-value for chi-square distribution."""
    if df <= 0:
        return 1.0
    
    if chi_square <= 0:
        return 1.0
    
    # Simple approximation using normal distribution for large df
    if df > 30:
        # Normal approximation
        mean = df
        variance = 2 * df
        z = (chi_square - mean) / math.sqrt(variance)
        return 1 - _standard_normal_cdf(z)
    
    # Rough approximation for smaller df
    # This is very approximate - real implementation would use gamma function
    if chi_square > df * 2:
        return 0.01  # Likely significant
    elif chi_square > df:
        return 0.1   # Moderately significant
    else:
        return 0.5   # Not significant


def _chi_square_critical_value(df: int, alpha: float) -> float:
    """Approximate critical value for chi-square distribution at given alpha."""
    # Very rough approximation
    if df == 1:
        return 3.841 if alpha == 0.05 else 6.635 if alpha == 0.01 else 10.828
    elif df == 2:
        return 5.991 if alpha == 0.05 else 9.210 if alpha == 0.01 else 13.816
    else:
        # Linear approximation (very rough)
        base = 3.841 if alpha == 0.05 else 6.635 if alpha == 0.01 else 10.828
        return base + (df - 1) * 1.5


def _standard_normal_cdf(z: float) -> float:
    """Approximate cumulative distribution function of standard normal."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


__all__ = ['chi_square_test']
