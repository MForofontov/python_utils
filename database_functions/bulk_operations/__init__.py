"""
Bulk database operations with chunking, progress tracking, and error handling.

This module provides workflow logic for efficiently handling large-scale database
operations with features like automatic chunking, error recovery, and progress tracking.
"""

from .execute_bulk_chunked import execute_bulk_chunked, BulkOperationResult

__all__ = [
    "BulkOperationResult",
    "execute_bulk_chunked",
]

from _version import __version__
