"""
Directory operations module: Directory creation, copying, and management utilities.

This module provides utilities for creating, copying, merging, and cleaning up
directories and their contents.
"""

from .cleanup import cleanup
from .copy_folder import copy_folder
from .create_directory import create_directory
from .merge_folders import merge_folders

__all__ = [
    'cleanup',
    'copy_folder',
    'create_directory',
    'merge_folders',
]

__version__ = '1.0.0'
