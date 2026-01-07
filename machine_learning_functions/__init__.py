"""
Machine Learning Utilities: Workflow helpers built on scikit-learn.

This module provides high-level utilities for common ML workflows,
built on top of scikit-learn with added convenience and validation.
"""

from .compare_models import compare_models
from .evaluate_model_performance import evaluate_model_performance
from .create_model_report import create_model_report

from .._version import __version__

__all__ = [
    'compare_models',
    'evaluate_model_performance',
    'create_model_report',
]
