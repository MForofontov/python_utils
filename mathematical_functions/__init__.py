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

from .basic import power
from .random import random_floats, random_integers, random_normal, random_sample

# Re-export main functions for convenience
# Statistics functions moved to external packages (scipy, numpy, statistics)

__all__ = [
    "power",
    "random_integers",
    "random_floats",
    "random_normal",
    "random_sample",
]
