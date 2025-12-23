"""
Connection management utilities with health checks and retry logic.

This module provides workflow logic for managing database connections with
automatic retry, health checks, and graceful cleanup.
"""

from .connection_pool_manager import ConnectionPoolManager
from .managed_db_connection import managed_db_connection

__all__ = [
    "ConnectionPoolManager",
    "managed_db_connection",
]

from _version import __version__
