"""
Scientific computing functions module.

This module provides comprehensive scientific computing utilities including:
- Statistical analysis (descriptive stats, hypothesis tests, correlations)
- Linear algebra operations (solving systems, eigenvalues, SVD, QR decomposition)
- Signal processing (filtering, FFT, spectrograms, resampling)
- Numerical methods (integration, differentiation, ODE solvers)
- Curve fitting (polynomial, nonlinear, spline interpolation)
"""

# Statistical analysis
from .bootstrap_statistic import bootstrap_statistic
from .comprehensive_stats import comprehensive_stats
from .correlation_analysis import correlation_analysis
from .multiple_testing_correction import multiple_testing_correction
from .perform_chi_square_test import perform_chi_square_test
from .perform_t_test import perform_t_test
from .robust_statistics import robust_statistics

# Linear algebra
from .compute_eigenvalues import compute_eigenvalues
from .compute_matrix_norm import compute_matrix_norm
from .compute_qr_decomposition import compute_qr_decomposition
from .compute_svd import compute_svd
from .solve_linear_system import solve_linear_system

# Signal processing
from .apply_filter import apply_filter
from .compute_fft import compute_fft
from .compute_spectrogram import compute_spectrogram
from .resample_signal import resample_signal

# Numerical methods
from .numerical_derivative import numerical_derivative
from .numerical_integration import numerical_integration
from .solve_ode import solve_ode

# Curve fitting
from .nonlinear_fit import nonlinear_fit
from .polynomial_fit import polynomial_fit
from .spline_interpolation import spline_interpolation

__all__ = [
    # Statistical analysis
    "bootstrap_statistic",
    "comprehensive_stats",
    "correlation_analysis",
    "multiple_testing_correction",
    "perform_chi_square_test",
    "perform_t_test",
    "robust_statistics",
    # Linear algebra
    "compute_eigenvalues",
    "compute_matrix_norm",
    "compute_qr_decomposition",
    "compute_svd",
    "solve_linear_system",
    # Signal processing
    "apply_filter",
    "compute_fft",
    "compute_spectrogram",
    "resample_signal",
    # Numerical methods
    "numerical_derivative",
    "numerical_integration",
    "solve_ode",
    # Curve fitting
    "nonlinear_fit",
    "polynomial_fit",
    "spline_interpolation",
]

# Version
from ._version import __version__
