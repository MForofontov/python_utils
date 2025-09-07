
"""JSON & Serialization Utilities module.

This module provides various utilities for working with JSON data,
including safe loading/dumping, pretty-printing, merging, and comparison.
"""

from .safe_json_load import safe_json_load
from .safe_json_dump import safe_json_dump
from .json_merge import json_merge
from .json_diff import json_diff

__all__ = [
    'safe_json_load',
    'safe_json_dump',
    'json_merge',
    'json_diff',
]
