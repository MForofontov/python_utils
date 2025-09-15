"""
File operations module: File reading, writing, copying, and management utilities.

This module provides utilities for basic file operations including reading,
writing, copying, deleting, and concatenating files.
"""

from .check_and_delete_file import check_and_delete_file
from .concat_files import concat_files
from .read_lines import read_lines
from .write_lines import write_lines

__all__ = [
    "check_and_delete_file",
    "concat_files",
    "read_lines",
    "write_lines",
]

__version__ = "1.0.0"
