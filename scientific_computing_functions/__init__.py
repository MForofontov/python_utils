"""
Scientific computing functions module.

This module provides comprehensive scientific computing utilities including:
- Statistical analysis (descriptive stats, hypothesis tests, correlations)
- Linear algebra operations (solving systems, SVD)
- Signal processing (filtering)
- Numerical methods (integration, differentiation)
"""

# Statistical analysis
from .statistical_analysis import *
# Linear algebra
from .linear_algebra import *
# Signal processing
from .signal_processing import *
# Numerical methods
from .numerical_methods import *

__all__ = [
    # Statistical analysis
    "bootstrap_statistic",
    "comprehensive_stats",
    "correlation_analysis",
    "perform_t_test",
    "robust_statistics",
    # Linear algebra
    "compute_svd",
    "solve_linear_system",
    # Signal processing
    "apply_filter",
    # Numerical methods
    "numerical_derivative",
    "numerical_integration",
]

# Version
from .._version import __version__
