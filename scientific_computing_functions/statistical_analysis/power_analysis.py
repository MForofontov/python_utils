"""Perform power analysis for sample size estimation."""

from typing import Literal

import numpy as np
from scipy import stats


def power_analysis(
    effect_size: float,
    alpha: float = 0.05,
    power: float = 0.8,
    test_type: Literal["t-test", "anova", "proportion", "correlation"] = "t-test",
    alternative: Literal["two-sided", "less", "greater"] = "two-sided",
    n_groups: int = 2,
) -> dict[str, float]:
    """
    Perform power analysis to estimate required sample size.

    Calculates the minimum sample size needed to achieve desired statistical power
    given an effect size and significance level. Implements power analysis workflow
    for multiple test types.

    Parameters
    ----------
    effect_size : float
        Expected effect size (Cohen's d for t-test, f for ANOVA, h for proportions, r for correlation).
    alpha : float, optional
        Significance level (by default 0.05).
    power : float, optional
        Desired statistical power (by default 0.8).
    test_type : Literal["t-test", "anova", "proportion", "correlation"], optional
        Type of statistical test (by default "t-test").
    alternative : Literal["two-sided", "less", "greater"], optional
        Type of alternative hypothesis (by default "two-sided").
    n_groups : int, optional
        Number of groups for ANOVA (by default 2).

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - required_sample_size: Minimum sample size per group
        - total_sample_size: Total sample size across all groups
        - effect_size: Input effect size
        - alpha: Input significance level
        - power: Input desired power

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> result = power_analysis(effect_size=0.5, alpha=0.05, power=0.8)
    >>> result['required_sample_size']
    64

    >>> result = power_analysis(effect_size=0.3, test_type="correlation")
    >>> result['required_sample_size'] > 60
    True

    Notes
    -----
    Effect size conventions (Cohen):
    - Small: d=0.2, f=0.1, h=0.2, r=0.1
    - Medium: d=0.5, f=0.25, h=0.5, r=0.3
    - Large: d=0.8, f=0.4, h=0.8, r=0.5

    Power analysis helps researchers determine adequate sample sizes before
    conducting studies, avoiding underpowered studies that waste resources.

    Complexity
    ----------
    Time: O(log n) due to binary search, Space: O(1)
    """
    # Input validation
    if not isinstance(effect_size, (int, float)):
        raise TypeError(f"effect_size must be a number, got {type(effect_size).__name__}")
    if not isinstance(alpha, (int, float)):
        raise TypeError(f"alpha must be a number, got {type(alpha).__name__}")
    if not isinstance(power, (int, float)):
        raise TypeError(f"power must be a number, got {type(power).__name__}")
    if not isinstance(test_type, str):
        raise TypeError(f"test_type must be a string, got {type(test_type).__name__}")
    if not isinstance(alternative, str):
        raise TypeError(f"alternative must be a string, got {type(alternative).__name__}")
    if not isinstance(n_groups, int):
        raise TypeError(f"n_groups must be an integer, got {type(n_groups).__name__}")

    if effect_size <= 0:
        raise ValueError(f"effect_size must be positive, got {effect_size}")
    if not 0 < alpha < 1:
        raise ValueError(f"alpha must be in (0, 1), got {alpha}")
    if not 0 < power < 1:
        raise ValueError(f"power must be in (0, 1), got {power}")
    if test_type not in ["t-test", "anova", "proportion", "correlation"]:
        raise ValueError(f"Invalid test_type: {test_type}")
    if alternative not in ["two-sided", "less", "greater"]:
        raise ValueError(f"Invalid alternative: {alternative}")
    if n_groups < 2:
        raise ValueError(f"n_groups must be >= 2, got {n_groups}")

    # Calculate critical values
    if alternative == "two-sided":
        z_alpha = stats.norm.ppf(1 - alpha / 2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)

    z_beta = stats.norm.ppf(power)

    # Calculate sample size based on test type
    if test_type == "t-test":
        # Cohen's formula for independent t-test
        required_n = int(np.ceil(2 * ((z_alpha + z_beta) / effect_size) ** 2))
        total_n = required_n * 2

    elif test_type == "anova":
        # Cohen's formula for ANOVA
        # effect_size is f (Cohen's f)
        lambda_param = effect_size**2 * n_groups
        required_n = int(np.ceil((z_alpha + z_beta) ** 2 / lambda_param))
        total_n = required_n * n_groups

    elif test_type == "proportion":
        # Cohen's formula for proportion test
        # effect_size is h (Cohen's h)
        required_n = int(np.ceil(((z_alpha + z_beta) / effect_size) ** 2))
        total_n = required_n * 2

    elif test_type == "correlation":
        # Fisher's z transformation for correlation
        # effect_size is r (correlation coefficient)
        z_r = 0.5 * np.log((1 + effect_size) / (1 - effect_size))
        required_n = int(np.ceil(((z_alpha + z_beta) / z_r) ** 2 + 3))
        total_n = required_n

    return {
        "required_sample_size": required_n,
        "total_sample_size": total_n,
        "effect_size": effect_size,
        "alpha": alpha,
        "power": power,
    }


__all__ = ["power_analysis"]
