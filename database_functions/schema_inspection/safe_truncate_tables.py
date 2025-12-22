"""
Safely truncate tables in dependency order respecting foreign keys.
"""

import logging
from typing import Any

from .get_foreign_key_dependencies import get_foreign_key_dependencies

logger = logging.getLogger(__name__)


def safe_truncate_tables(
    connection: Any,
    tables: list[str] | None = None,
    cascade: bool = False,
    schema: str | None = None,
) -> dict[str, Any]:
    """
    Truncate tables in safe order respecting foreign key dependencies.

    Essential for test cleanup, data refresh, and staging environment resets.
    Automatically determines correct order to avoid FK constraint violations.

    Parameters
    ----------
    connection : Any
        Database connection.
    tables : list[str] | None, optional
        Specific tables to truncate, None for all (by default None).
    cascade : bool, optional
        Use CASCADE option if supported by database (by default False).
    schema : str | None, optional
        Schema name (by default None).

    Returns
    -------
    dict[str, Any]
        Results with truncated tables, order used, and any errors.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> result = safe_truncate_tables(conn, tables=["orders", "customers"])
    >>> print(f"Truncated {len(result['truncated'])} tables")

    Notes
    -----
    Uses DELETE instead of TRUNCATE for databases that don't support it.
    Respects foreign key dependencies to prevent constraint violations.

    Complexity
    ----------
    Time: O(n) where n is number of tables, Space: O(n)
    """
    # Input validation
    if connection is None:
        raise TypeError("connection cannot be None")
    if tables is not None and not isinstance(tables, list):
        raise TypeError(f"tables must be list or None, got {type(tables).__name__}")
    if not isinstance(cascade, bool):
        raise TypeError(f"cascade must be bool, got {type(cascade).__name__}")
    if schema is not None and not isinstance(schema, str):
        raise TypeError(f"schema must be str or None, got {type(schema).__name__}")

    # Get dependency order
    deps = get_foreign_key_dependencies(connection, schema=schema)
    ordered_tables = deps["ordered_tables"]
    
    # Filter to requested tables if specified
    if tables is not None:
        tables_set = set(tables)
        ordered_tables = [t for t in ordered_tables if t in tables_set]

    truncated = []
    errors = []
    
    # Truncate in reverse order (dependents first)
    for table in reversed(ordered_tables):
        try:
            # Try TRUNCATE first
            cascade_clause = " CASCADE" if cascade else ""
            truncate_sql = f"TRUNCATE TABLE {table}{cascade_clause}"
            
            try:
                connection.execute(truncate_sql)
                truncated.append(table)
                logger.info(f"Truncated table: {table}")
            except Exception as truncate_error:
                # Fall back to DELETE if TRUNCATE not supported
                logger.warning(f"TRUNCATE failed for {table}, using DELETE: {truncate_error}")
                delete_sql = f"DELETE FROM {table}"
                connection.execute(delete_sql)
                truncated.append(table)
                logger.info(f"Deleted all rows from table: {table}")
                
        except Exception as e:
            error_msg = f"Failed to truncate {table}: {e}"
            logger.error(error_msg)
            errors.append({"table": table, "error": str(e)})

    # Commit if in transaction
    try:
        if hasattr(connection, 'commit'):
            connection.commit()
    except Exception:
        pass  # Already in autocommit mode

    return {
        "truncated": truncated,
        "order_used": list(reversed(ordered_tables)),
        "errors": errors,
        "success": len(errors) == 0
    }


__all__ = ['safe_truncate_tables']
