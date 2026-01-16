"""
Detect drift between actual database schema and expected schema definition.
"""

import logging
from typing import Any

from sqlalchemy import inspect

from .get_table_info import TableInfo

logger = logging.getLogger(__name__)


def detect_schema_drift(
    connection: Any,
    expected_schema: dict[str, TableInfo],
    schema: str | None = None,
) -> dict[str, Any]:
    """
    Detect drift between actual database schema and expected schema definition.

    Parameters
    ----------
    connection : Any
        Database connection.
    expected_schema : dict[str, TableInfo]
        Expected schema definition (table name -> TableInfo).
    schema : str | None, optional
        Schema name to check (by default None).

    Returns
    -------
    dict[str, Any]
        Dictionary with drift detection results.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> expected = {
    ...     "users": {
    ...         "name": "users",
    ...         "columns": [
    ...             {"name": "id", "type": "INTEGER", "primary_key": True},
    ...             {"name": "name", "type": "VARCHAR(255)"}
    ...         ]
    ...     }
    ... }
    >>> drift = detect_schema_drift(conn, expected)
    >>> if drift['has_drift']:
    ...     print(f"Schema drift detected: {drift['summary']}")

    Complexity
    ----------
    Time: O(n*m) where n is tables, m is columns, Space: O(n*m)
    """
    # Input validation
    if connection is None:
        raise TypeError("connection cannot be None")
    if not isinstance(expected_schema, dict):
        raise TypeError(
            f"expected_schema must be dict, got {type(expected_schema).__name__}"
        )
    if schema is not None and not isinstance(schema, str):
        raise TypeError(f"schema must be str or None, got {type(schema).__name__}")

    inspector = inspect(connection)
    actual_tables = set(inspector.get_table_names(schema=schema))
    expected_tables = set(expected_schema.keys())

    missing_tables = list(expected_tables - actual_tables)
    unexpected_tables = list(actual_tables - expected_tables)
    common_tables = expected_tables & actual_tables

    table_diffs = []

    for table_name in common_tables:
        expected_info = expected_schema[table_name]
        actual_cols = {
            col["name"]: col for col in inspector.get_columns(table_name, schema=schema)
        }
        expected_cols = {col["name"]: col for col in expected_info["columns"]}

        missing_cols = set(expected_cols.keys()) - set(actual_cols.keys())
        unexpected_cols = set(actual_cols.keys()) - set(expected_cols.keys())

        if missing_cols or unexpected_cols:
            table_diffs.append(
                {
                    "table": table_name,
                    "missing_columns": list(missing_cols),
                    "unexpected_columns": list(unexpected_cols),
                }
            )

    has_drift = bool(missing_tables or unexpected_tables or table_diffs)

    result = {
        "has_drift": has_drift,
        "missing_tables": missing_tables,
        "unexpected_tables": unexpected_tables,
        "table_diffs": table_diffs,
        "summary": (
            f"{len(missing_tables)} missing tables, "
            f"{len(unexpected_tables)} unexpected tables, "
            f"{len(table_diffs)} tables with column differences"
        ),
    }

    logger.info(f"Schema drift detection: has_drift={has_drift}, {result['summary']}")

    return result


__all__ = ["detect_schema_drift"]
