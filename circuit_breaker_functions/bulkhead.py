"""
Bulkhead pattern for resource isolation and preventing resource exhaustion.
"""

import threading
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class Bulkhead:
    """
    Bulkhead pattern for resource isolation.

    The bulkhead pattern isolates critical resources to prevent one component
    from consuming all available resources and causing system-wide failure.
    It limits concurrent access to a resource using a semaphore.

    Attributes
    ----------
    max_concurrent : int
        Maximum number of concurrent operations allowed.
    timeout : float | None
        Maximum time to wait for resource availability.

    Parameters
    ----------
    max_concurrent : int
        Maximum concurrent operations (by default 10).
    timeout : float | None, optional
        Timeout in seconds to acquire resource (by default None).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> bulkhead = Bulkhead(max_concurrent=5, timeout=10.0)
    >>> def database_query():
    ...     return "result"
    >>> result = bulkhead.call(database_query)
    'result'

    >>> # Prevents more than 5 concurrent database calls
    >>> with bulkhead:
    ...     # Protected operation
    ...     pass

    Notes
    -----
    The bulkhead pattern is named after ship compartments that prevent
    flooding from spreading. It isolates failures and prevents cascading
    resource exhaustion.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """

    def __init__(
        self,
        max_concurrent: int = 10,
        timeout: float | None = None,
    ) -> None:
        """Initialize bulkhead with concurrency limit."""
        # Type validation
        if not isinstance(max_concurrent, int):
            raise TypeError(
                f"max_concurrent must be an integer, got {type(max_concurrent).__name__}"
            )
        if timeout is not None and not isinstance(timeout, (int, float)):
            raise TypeError(
                f"timeout must be a number or None, got {type(timeout).__name__}"
            )

        # Value validation
        if max_concurrent <= 0:
            raise ValueError(f"max_concurrent must be positive, got {max_concurrent}")
        if timeout is not None and timeout <= 0:
            raise ValueError(f"timeout must be positive, got {timeout}")

        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self._semaphore = threading.Semaphore(max_concurrent)
        self._active_count = 0
        self._lock = threading.Lock()

    def call(self, func: Callable[[], T], *args: Any, **kwargs: Any) -> T:
        """
        Execute function with resource isolation.

        Parameters
        ----------
        func : Callable
            Function to execute.
        *args : Any
            Positional arguments for the function.
        **kwargs : Any
            Keyword arguments for the function.

        Returns
        -------
        T
            Result of the function call.

        Raises
        ------
        TypeError
            If func is not callable.
        TimeoutError
            If unable to acquire resource within timeout.
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")

        acquired = self._semaphore.acquire(timeout=self.timeout)
        if not acquired:
            raise TimeoutError(
                f"Unable to acquire resource within {self.timeout}s. "
                f"Maximum {self.max_concurrent} concurrent operations allowed."
            )

        try:
            with self._lock:
                self._active_count += 1
            return func(*args, **kwargs)
        finally:
            with self._lock:
                self._active_count -= 1
            self._semaphore.release()

    def __enter__(self) -> "Bulkhead":
        """Context manager entry."""
        acquired = self._semaphore.acquire(timeout=self.timeout)
        if not acquired:
            raise TimeoutError(
                f"Unable to acquire resource within {self.timeout}s. "
                f"Maximum {self.max_concurrent} concurrent operations allowed."
            )
        with self._lock:
            self._active_count += 1
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        with self._lock:
            self._active_count -= 1
        self._semaphore.release()

    @property
    def active_count(self) -> int:
        """
        Get current number of active operations.

        Returns
        -------
        int
            Number of currently active operations.

        Examples
        --------
        >>> bulkhead = Bulkhead(max_concurrent=5)
        >>> bulkhead.active_count
        0
        """
        with self._lock:
            return self._active_count

    @property
    def available_slots(self) -> int:
        """
        Get number of available slots for new operations.

        Returns
        -------
        int
            Number of available slots.

        Examples
        --------
        >>> bulkhead = Bulkhead(max_concurrent=5)
        >>> bulkhead.available_slots
        5
        """
        with self._lock:
            return self.max_concurrent - self._active_count


__all__ = ["Bulkhead"]
