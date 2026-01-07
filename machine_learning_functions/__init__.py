"""
Machine Learning Utilities: Workflow helpers built on scikit-learn.

This module provides high-level utilities for common ML workflows,
built on top of scikit-learn with added convenience and validation.
"""

from .compare_models import compare_models
from .evaluate_model_performance import evaluate_model_performance
from .create_model_report import create_model_report
from .extract_feature_importance import extract_feature_importance
from .analyze_predictions import analyze_predictions
from .detect_overfitting import detect_overfitting
from .calculate_prediction_intervals import calculate_prediction_intervals
from .auto_select_best_model import auto_select_best_model

from .._version import __version__

__all__ = [
    'compare_models',
    'evaluate_model_performance',
    'create_model_report',
    'extract_feature_importance',
    'analyze_predictions',
    'detect_overfitting',
    'calculate_prediction_intervals',
    'auto_select_best_model',
]
