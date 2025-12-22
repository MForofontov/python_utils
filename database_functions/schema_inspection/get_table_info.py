"""
Get comprehensive information about a database table.
"""

import logging
from typing import Any, TypedDict

from sqlalchemy import inspect

logger = logging.getLogger(__name__)


class ColumnInfo(TypedDict, total=False):
    """Information about a database column."""

    name: str
    type: str
    nullable: bool
    default: Any
    primary_key: bool


class TableInfo(TypedDict):
    """Information about a database table."""

    name: str
    columns: list[ColumnInfo]
    indexes: list[dict[str, Any]]
    foreign_keys: list[dict[str, Any]]


def get_table_info(
    connection: Any,
    table_name: str,
    schema: str | None = None,
) -> TableInfo:
    """
    Get comprehensive information about a database table.

    Parameters
    ----------
    connection : Any
        Database connection object.
    table_name : str
        Name of the table to inspect.
    schema : str | None, optional
        Schema name (by default None for default schema).

    Returns
    -------
    TableInfo
        Dictionary containing table structure information.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If table doesn't exist.

    Examples
    --------
    >>> info = get_table_info(conn, "users")
    >>> print(f"Table has {len(info['columns'])} columns")
    >>> for col in info['columns']:
    ...     print(f"  {col['name']}: {col['type']}")

    Complexity
    ----------
    Time: O(n) where n is number of columns, Space: O(n)
    """
    # Input validation
    if connection is None:
        raise TypeError("connection cannot be None")
    if not isinstance(table_name, str):
        raise TypeError(f"table_name must be str, got {type(table_name).__name__}")
    if not table_name:
        raise ValueError("table_name cannot be empty")
    if schema is not None and not isinstance(schema, str):
        raise TypeError(f"schema must be str or None, got {type(schema).__name__}")

    inspector = inspect(connection)

    # Check if table exists
    tables = inspector.get_table_names(schema=schema)
    if table_name not in tables:
        raise ValueError(f"Table '{table_name}' not found in schema '{schema or 'default'}'")

    # Get column information
    columns_raw = inspector.get_columns(table_name, schema=schema)
    columns: list[ColumnInfo] = []
    for col in columns_raw:
        col_info: ColumnInfo = {
            "name": col["name"],
            "type": str(col["type"]),
            "nullable": col.get("nullable", True),
            "default": col.get("default"),
            "primary_key": col.get("primary_key", False),
        }
        columns.append(col_info)

    # Get indexes
    indexes_raw = inspector.get_indexes(table_name, schema=schema)
    indexes = [
        {
            "name": idx.get("name"),
            "columns": idx.get("column_names", []),
            "unique": idx.get("unique", False),
        }
        for idx in indexes_raw
    ]

    # Get foreign keys
    fks_raw = inspector.get_foreign_keys(table_name, schema=schema)
    foreign_keys = [
        {
            "name": fk.get("name"),
            "columns": fk.get("constrained_columns", []),
            "referred_table": fk.get("referred_table"),
            "referred_columns": fk.get("referred_columns", []),
        }
        for fk in fks_raw
    ]

    result: TableInfo = {
        "name": table_name,
        "columns": columns,
        "indexes": indexes,
        "foreign_keys": foreign_keys,
    }

    logger.debug(
        f"Retrieved info for table '{table_name}': "
        f"{len(columns)} columns, {len(indexes)} indexes, {len(foreign_keys)} foreign keys"
    )

    return result


__all__ = ["ColumnInfo", "TableInfo", "get_table_info"]
