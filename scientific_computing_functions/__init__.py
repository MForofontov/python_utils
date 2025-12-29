"""
Scientific computing functions module.

This module provides comprehensive scientific computing utilities including:
- Statistical analysis (descriptive stats, hypothesis tests, correlations)
- Linear algebra operations (solving systems, SVD)
- Signal processing (filtering, spectrograms)
- Numerical methods (integration, differentiation)
- Curve fitting (polynomial, nonlinear)
"""

# Statistical analysis
from .bootstrap_statistic import bootstrap_statistic
from .comprehensive_stats import comprehensive_stats
from .correlation_analysis import correlation_analysis
from .multiple_testing_correction import multiple_testing_correction
from .perform_t_test import perform_t_test
from .robust_statistics import robust_statistics

# Linear algebra
from .compute_svd import compute_svd
from .solve_linear_system import solve_linear_system

# Signal processing
from .apply_filter import apply_filter
from .compute_spectrogram import compute_spectrogram

# Numerical methods
from .numerical_derivative import numerical_derivative
from .numerical_integration import numerical_integration

# Curve fitting
from .nonlinear_fit import nonlinear_fit
from .polynomial_fit import polynomial_fit

__all__ = [
    # Statistical analysis
    "bootstrap_statistic",
    "comprehensive_stats",
    "correlation_analysis",
    "multiple_testing_correction",
    "perform_t_test",
    "robust_statistics",
    # Linear algebra
    "compute_svd",
    "solve_linear_system",
    # Signal processing
    "apply_filter",
    "compute_spectrogram",
    # Numerical methods
    "numerical_derivative",
    "numerical_integration",
    # Curve fitting
    "nonlinear_fit",
    "polynomial_fit",
]

# Version
from .._version import __version__
