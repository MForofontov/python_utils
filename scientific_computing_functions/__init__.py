"""
Scientific computing functions module.

This module provides comprehensive scientific computing utilities including:
- Statistical analysis (descriptive stats, hypothesis tests, correlations, outliers, power analysis)
- Linear algebra operations (solving systems, SVD, constrained least squares)
- Signal processing (filtering, adaptive filtering)
- Numerical methods (integration, differentiation, boundary value problems)
"""

# Statistical analysis
# Linear algebra
from .linear_algebra import (
    compute_svd,
    constrained_least_squares,
    solve_linear_system,
)

# Numerical methods
from .numerical_methods import (
    numerical_derivative,
    numerical_integration,
    solve_boundary_value_problem,
)

# Signal processing
from .signal_processing import (
    adaptive_filter,
    apply_filter,
)
from .statistical_analysis import (
    bootstrap_statistic,
    comprehensive_stats,
    correlation_analysis,
    detect_outliers,
    perform_t_test,
    power_analysis,
    robust_statistics,
)

__all__ = [
    # Statistical analysis
    "bootstrap_statistic",
    "comprehensive_stats",
    "correlation_analysis",
    "detect_outliers",
    "perform_t_test",
    "power_analysis",
    "robust_statistics",
    # Linear algebra
    "compute_svd",
    "constrained_least_squares",
    "solve_linear_system",
    # Signal processing
    "adaptive_filter",
    "apply_filter",
    # Numerical methods
    "numerical_derivative",
    "numerical_integration",
    "solve_boundary_value_problem",
]
