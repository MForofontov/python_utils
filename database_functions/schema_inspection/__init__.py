"""
Database schema inspection and comparison utilities.

This module provides workflow logic for analyzing database schemas,
comparing structures, detecting drift, and performing data quality checks.
"""

from .check_data_anomalies import check_data_anomalies
from .check_encoding_issues import check_encoding_issues
from .compare_schemas import compare_schemas, SchemaComparison
from .compare_table_data import compare_table_data
from .detect_schema_drift import detect_schema_drift
from .find_duplicate_indexes import find_duplicate_indexes
from .find_duplicate_rows import find_duplicate_rows
from .find_missing_indexes import find_missing_indexes
from .find_unused_columns import find_unused_columns
from .get_column_statistics import get_column_statistics
from .get_foreign_key_dependencies import get_foreign_key_dependencies
from .get_table_info import get_table_info, ColumnInfo, TableInfo
from .get_table_sizes import get_table_sizes
from .safe_truncate_tables import safe_truncate_tables
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
    "safe_truncate_tables",
    "find_duplicate_rows",
    "get_table_sizes",
    "check_encoding_issues",
    "find_unused_columns",
    "find_missing_indexes",
    "compare_table_data",
    "check_data_anomalies",
]

from ..._version import __version__
