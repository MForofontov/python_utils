"""
Database utility workflows.

This module provides workflow logic and patterns for database operations,
adding value on top of battle-tested packages like SQLAlchemy, psycopg2, pymongo.

Key Focus Areas:
- Connection management with health checks and retry logic
- Bulk operations with chunking, progress tracking, and error handling
- Query utilities with timeout management and result streaming
- Transaction coordination with savepoint management
- Schema inspection and comparison utilities
"""

from .connection_management import ConnectionPoolManager, managed_db_connection
from .bulk_operations import (
    BulkOperationResult,
    execute_bulk_chunked,
)
from .query_execution import (
    QueryTimeoutError,
    execute_with_retry,
    stream_query_results,
    execute_with_timeout,
)
from .transaction_management import (
    atomic_transaction,
    nested_transaction,
    savepoint_context,
)
from .schema_inspection import (
    ColumnInfo,
    TableInfo,
    SchemaComparison,
    get_table_info,
    compare_schemas,
    detect_schema_drift,
)

__all__ = [
    # Connection management
    "ConnectionPoolManager",
    "managed_db_connection",
    # Bulk operations
    "BulkOperationResult",
    "execute_bulk_chunked",
    # Query execution
    "QueryTimeoutError",
    "execute_with_retry",
    "stream_query_results",
    "execute_with_timeout",
    # Transaction management
    "atomic_transaction",
    "nested_transaction",
    "savepoint_context",
    # Schema inspection
    "ColumnInfo",
    "TableInfo",
    "SchemaComparison",
    "get_table_info",
    "compare_schemas",
    "detect_schema_drift",
]

from .._version import __version__
