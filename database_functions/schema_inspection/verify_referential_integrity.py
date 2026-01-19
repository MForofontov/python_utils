"""
Verify referential integrity by finding orphaned records.
"""

import logging
from typing import Any

from sqlalchemy import MetaData, and_, func, inspect, not_, select

logger = logging.getLogger(__name__)


def verify_referential_integrity(
    connection: Any,
    schema: str | None = None,
) -> list[dict[str, Any]]:
    """
    Check for foreign key constraint violations (orphaned records).

    Finds records that reference non-existent parent records. Useful for
    data quality audits and fixing legacy data before adding constraints.

    Parameters
    ----------
    connection : Any
        Database connection.
    schema : str | None, optional
        Schema name to check (by default None).

    Returns
    -------
    list[dict[str, Any]]
        List of violations, each containing:
        - 'table': Table with orphaned records
        - 'column': Foreign key column
        - 'referenced_table': Expected parent table
        - 'orphaned_count': Number of orphaned records
        - 'sample_ids': Sample orphaned IDs (up to 10)

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> violations = verify_referential_integrity(conn)
    >>> for v in violations:
    ...     print(f"{v['table']}.{v['column']}: {v['orphaned_count']} orphaned")
    ...     print(f"Sample IDs: {v['sample_ids']}")

    Notes
    -----
    Critical for data migration and constraint enforcement.
    Can be slow on large tables - consider adding WHERE clauses for subsets.

    Complexity
    ----------
    Time: O(n*m) where n is tables, m is avg rows, Space: O(k) where k is violations
    """
    # Input validation
    if connection is None:
        raise TypeError("connection cannot be None")
    if schema is not None and not isinstance(schema, str):
        raise TypeError(f"schema must be str or None, got {type(schema).__name__}")

    inspector = inspect(connection)
    tables = inspector.get_table_names(schema=schema)
    violations = []

    # Reflect metadata for SQLAlchemy table objects
    metadata = MetaData()
    metadata.reflect(bind=connection, schema=schema)

    for table_name in tables:
        if table_name not in metadata.tables:
            continue

        table = metadata.tables[table_name]
        fks = inspector.get_foreign_keys(table_name, schema=schema)

        for fk in fks:
            constrained_columns = fk.get("constrained_columns", [])
            referred_table_name = fk.get("referred_table")
            referred_columns = fk.get("referred_columns", [])

            if (
                not constrained_columns
                or not referred_table_name
                or not referred_columns
            ):
                continue

            # Get table objects
            if referred_table_name not in metadata.tables:
                continue

            referred_table = metadata.tables[referred_table_name]
            fk_column = table.c[constrained_columns[0]]
            ref_column = referred_table.c[referred_columns[0]]

            try:
                # Build subquery for valid references
                select(ref_column).subquery()

                # Find orphaned records using SQLAlchemy expressions
                orphaned_query = (
                    select(fk_column, func.count().label("cnt"))
                    .where(
                        and_(
                            fk_column.isnot(None),
                            not_(fk_column.in_(select(ref_column))),
                        )
                    )
                    .group_by(fk_column)
                    .limit(10)
                )

                result = connection.execute(orphaned_query)
                orphaned = result.fetchall()

                if orphaned:
                    # Get total count of orphaned records
                    count_query = (
                        select(func.count())
                        .select_from(table)
                        .where(
                            and_(
                                fk_column.isnot(None),
                                not_(fk_column.in_(select(ref_column))),
                            )
                        )
                    )
                    total_result = connection.execute(count_query)
                    total_count = total_result.scalar()

                    violations.append(
                        {
                            "table": table_name,
                            "column": constrained_columns[0],
                            "referenced_table": referred_table_name,
                            "referenced_column": referred_columns[0],
                            "orphaned_count": total_count,
                            "sample_ids": [row[0] for row in orphaned],
                        }
                    )
            except Exception as e:
                logger.warning(
                    f"Could not check {table_name}.{constrained_columns[0]}: {e}"
                )
                continue

    return violations


__all__ = ["verify_referential_integrity"]
