"""
Mathematical functions package.

This package provides comprehensive mathematical, statistical, and advanced computational
functions organized into logical submodules. Each function supports multiple methods
and algorithms where applicable.

Submodules:
    basic: Basic mathematical operations with multiple algorithms
    advanced: Advanced mathematical computations and algorithms  
    statistics: Statistical functions with various methods
    random: Random number generation and sampling functions
"""

# Import from all submodules
from .basic import *
from .statistics import *
from .random import *

# Re-export main functions for convenience
from .statistics.mean import mean
from .statistics.median import median, weighted_median
from .statistics.mode import mode
from .statistics.stddev import stddev
from .statistics.variance import variance
from .statistics.range_value import range_value
from .statistics.quantile import quantile
from .statistics.skewness import skewness
from .statistics.correlation_analysis import correlation_analysis
from .statistics.correlation_coefficient import correlation_coefficient
from .statistics.time_series_analysis import time_series_analysis
from .statistics.linear_regression import linear_regression
from .statistics.chi_square_test import chi_square_test
from .statistics.outlier_detection import outlier_detection

__all__ = [
    # Basic math operations
    "power",
    
    # Statistics
    "mean", "median", "weighted_median", "mode", "stddev", "variance", 
    "range_value", "quantile", "skewness",
    
    # Correlation and analysis
    "correlation_analysis", "correlation_coefficient",
    "time_series_analysis", "linear_regression",
    
    # Statistical tests
    "chi_square_test", "outlier_detection",
    
    # Random generators
    "random_integers", "random_floats", "random_normal", "random_sample",
]