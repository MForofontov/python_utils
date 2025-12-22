"""
Database schema inspection and comparison utilities.

This module provides workflow logic for analyzing database schemas,
comparing structures, detecting drift, and performing data quality checks.
"""

from .compare_schemas import compare_schemas, SchemaComparison
from .detect_schema_drift import detect_schema_drift
from .find_duplicate_indexes import find_duplicate_indexes
from .get_column_statistics import get_column_statistics
from .get_foreign_key_dependencies import get_foreign_key_dependencies
from .get_table_info import get_table_info, ColumnInfo, TableInfo
from .verify_referential_integrity import verify_referential_integrity

__all__ = [
    "ColumnInfo",
    "TableInfo",
    "SchemaComparison",
    "get_table_info",
    "compare_schemas",
    "detect_schema_drift",
    "get_foreign_key_dependencies",
    "verify_referential_integrity",
    "get_column_statistics",
    "find_duplicate_indexes",
]

__version__ = "1.0.0"
