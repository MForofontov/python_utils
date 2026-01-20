"""
Bulk database operations with chunking, progress tracking, and error handling.

This module provides workflow logic for efficiently handling large-scale database
operations with features like automatic chunking, error recovery, and progress tracking.
"""

from .execute_bulk_chunked import BulkOperationResult, execute_bulk_chunked

__all__ = [
    "BulkOperationResult",
    "execute_bulk_chunked",
]
