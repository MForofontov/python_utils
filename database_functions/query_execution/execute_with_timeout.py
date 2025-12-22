"""
Execute query with timeout limit.
"""

import logging
import signal
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class QueryTimeoutError(Exception):
    """Raised when a query execution exceeds the timeout limit."""

    pass


def execute_with_timeout(
    execute_func: Callable[[], T],
    timeout_seconds: float,
) -> T:
    """
    Execute a query with a timeout limit.

    Parameters
    ----------
    execute_func : Callable[[], T]
        Function that executes the query.
    timeout_seconds : float
        Maximum execution time in seconds.

    Returns
    -------
    T
        Result from execute_func.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    QueryTimeoutError
        If execution exceeds the timeout.

    Examples
    --------
    >>> def query_func():
    ...     return conn.execute("SELECT * FROM users")
    >>> try:
    ...     result = execute_with_timeout(query_func, timeout_seconds=5.0)
    ... except QueryTimeoutError:
    ...     print("Query took too long!")

    Notes
    -----
    - Uses signal.alarm for timeout enforcement (Unix only)
    - On Windows, this provides best-effort timeout checking
    - Query may not be immediately cancelled on all database drivers

    Complexity
    ----------
    Time: O(1) overhead, Space: O(1)
    """
    # Input validation
    if not callable(execute_func):
        raise TypeError("execute_func must be callable")
    if not isinstance(timeout_seconds, (int, float)):
        raise TypeError(f"timeout_seconds must be a number, got {type(timeout_seconds).__name__}")
    if timeout_seconds <= 0:
        raise ValueError(f"timeout_seconds must be positive, got {timeout_seconds}")

    def timeout_handler(signum: int, frame: Any) -> None:
        raise QueryTimeoutError(f"Query execution exceeded {timeout_seconds} seconds")

    # Set up signal handler (Unix systems only)
    try:
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout_seconds))

        try:
            result = execute_func()
            signal.alarm(0)  # Cancel alarm
            return result

        except QueryTimeoutError:
            logger.error(f"Query timed out after {timeout_seconds} seconds")
            raise

        finally:
            signal.alarm(0)  # Ensure alarm is cancelled
            signal.signal(signal.SIGALRM, old_handler)  # Restore old handler

    except (AttributeError, ValueError):
        # signal.alarm not available (Windows) or invalid timeout
        # Fall back to simple execution with warning
        logger.warning(
            "Signal-based timeout not available on this platform. "
            "Executing query without timeout enforcement."
        )
        return execute_func()


__all__ = ["QueryTimeoutError", "execute_with_timeout"]
