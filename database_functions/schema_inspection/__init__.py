"""
Database schema inspection and comparison utilities.

This module provides workflow logic for analyzing database schemas,
comparing structures, and detecting schema drift.
"""

from .compare_schemas import compare_schemas, SchemaComparison
from .detect_schema_drift import detect_schema_drift
from .get_table_info import get_table_info, ColumnInfo, TableInfo

__all__ = [
    "ColumnInfo",
    "TableInfo",
    "SchemaComparison",
    "get_table_info",
    "compare_schemas",
    "detect_schema_drift",
]

__version__ = "1.0.0"
