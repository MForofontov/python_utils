"""
Compare schemas between two databases.
"""

import logging
from typing import Any, TypedDict

from sqlalchemy import inspect

logger = logging.getLogger(__name__)


class SchemaComparison(TypedDict):
    """Result of schema comparison."""

    new_tables: list[str]
    dropped_tables: list[str]
    modified_tables: list[dict[str, Any]]
    severity: str


def compare_schemas(
    source_connection: Any,
    target_connection: Any,
    ignore_tables: set[str] | None = None,
    schema: str | None = None,
) -> SchemaComparison:
    """
    Compare schemas between two databases.

    Parameters
    ----------
    source_connection : Any
        Source database connection.
    target_connection : Any
        Target database connection.
    ignore_tables : set[str] | None, optional
        Set of table names to exclude from comparison.
    schema : str | None, optional
        Schema name to compare (by default None).

    Returns
    -------
    SchemaComparison
        Dictionary containing schema differences.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> comparison = compare_schemas(old_conn, new_conn)
    >>> if comparison['severity'] == 'breaking':
    ...     print("Warning: Breaking changes detected!")
    >>> for table in comparison['dropped_tables']:
    ...     print(f"  Table dropped: {table}")

    Complexity
    ----------
    Time: O(n*m) where n is tables, m is columns per table, Space: O(n*m)
    """
    # Input validation
    if source_connection is None:
        raise TypeError("source_connection cannot be None")
    if target_connection is None:
        raise TypeError("target_connection cannot be None")
    if ignore_tables is not None and not isinstance(ignore_tables, set):
        raise TypeError(f"ignore_tables must be set or None, got {type(ignore_tables).__name__}")
    if schema is not None and not isinstance(schema, str):
        raise TypeError(f"schema must be str or None, got {type(schema).__name__}")

    source_inspector = inspect(source_connection)
    target_inspector = inspect(target_connection)

    # Get table names
    source_tables = set(source_inspector.get_table_names(schema=schema))
    target_tables = set(target_inspector.get_table_names(schema=schema))

    # Apply ignore filter
    if ignore_tables:
        source_tables -= ignore_tables
        target_tables -= ignore_tables

    # Identify table changes
    new_tables = list(target_tables - source_tables)
    dropped_tables = list(source_tables - target_tables)
    common_tables = source_tables & target_tables

    modified_tables: list[dict[str, Any]] = []
    severity = "safe"

    # Compare common tables
    for table_name in common_tables:
        source_cols = {
            col["name"]: col
            for col in source_inspector.get_columns(table_name, schema=schema)
        }
        target_cols = {
            col["name"]: col
            for col in target_inspector.get_columns(table_name, schema=schema)
        }

        new_cols = set(target_cols.keys()) - set(source_cols.keys())
        dropped_cols = set(source_cols.keys()) - set(target_cols.keys())
        common_cols = set(source_cols.keys()) & set(target_cols.keys())

        type_changes = []
        for col_name in common_cols:
            source_type = str(source_cols[col_name]["type"])
            target_type = str(target_cols[col_name]["type"])
            if source_type != target_type:
                type_changes.append(
                    {
                        "column": col_name,
                        "old_type": source_type,
                        "new_type": target_type,
                    }
                )

        # Detect breaking changes
        if dropped_cols or type_changes:
            severity = "breaking"

        # Record changes for this table
        if new_cols or dropped_cols or type_changes:
            modified_tables.append(
                {
                    "table": table_name,
                    "new_columns": list(new_cols),
                    "dropped_columns": list(dropped_cols),
                    "type_changes": type_changes,
                }
            )

    # Dropped tables are breaking changes
    if dropped_tables:
        severity = "breaking"

    result: SchemaComparison = {
        "new_tables": new_tables,
        "dropped_tables": dropped_tables,
        "modified_tables": modified_tables,
        "severity": severity,
    }

    logger.info(
        f"Schema comparison complete: {len(new_tables)} new tables, "
        f"{len(dropped_tables)} dropped tables, {len(modified_tables)} modified tables, "
        f"severity={severity}"
    )

    return result


__all__ = ["SchemaComparison", "compare_schemas"]
