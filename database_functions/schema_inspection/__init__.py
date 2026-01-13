"""
Database schema inspection and comparison utilities.

This module provides workflow logic for analyzing database schemas,
comparing structures, detecting drift, and performing data quality checks.
"""

from .analyze_column_cardinality import analyze_column_cardinality
from .check_data_anomalies import check_data_anomalies
from .check_encoding_issues import check_encoding_issues
from .check_sequence_health import check_sequence_health
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
from .migrate_id_type import migrate_id_type
from .safe_truncate_tables import safe_truncate_tables
from .suggest_data_type_optimizations import suggest_data_type_optimizations
from .verify_referential_integrity import verify_referential_integrity

__all__ = [
    "ColumnInfo",
    "TableInfo",
    "SchemaComparison",
    "analyze_column_cardinality",
    "check_data_anomalies",
    "check_encoding_issues",
    "check_sequence_health",
    "compare_schemas",
    "compare_table_data",
    "detect_schema_drift",
    "find_duplicate_indexes",
    "find_duplicate_rows",
    "find_missing_indexes",
    "find_unused_columns",
    "get_column_statistics",
    "get_foreign_key_dependencies",
    "get_table_info",
    "get_table_sizes",
    "migrate_id_type",
    "safe_truncate_tables",
    "suggest_data_type_optimizations",
    "verify_referential_integrity",
]


