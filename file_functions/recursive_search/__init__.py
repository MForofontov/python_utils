"""
Recursive search module: Find files recursively with various criteria.

This module provides utilities for searching files recursively in directories
based on different criteria like extension, pattern, size, and modification time.
"""

from .find_files_by_extension import find_files_by_extension
from .find_files_by_mtime import find_files_by_mtime
from .find_files_by_pattern import find_files_by_pattern
from .find_files_by_size import find_files_by_size

__all__ = [
    "find_files_by_extension",
    "find_files_by_pattern",
    "find_files_by_size",
    "find_files_by_mtime",
]

__version__ = "1.0.0"
