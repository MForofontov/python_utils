"""
Adaptive timeout that self-adjusts based on historical latency.
"""

import time
from collections import deque
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class AdaptiveTimeout:
    """
    Self-adjusting timeout based on historical latency measurements.

    The adaptive timeout tracks execution times and automatically adjusts
    the timeout threshold based on percentile statistics, preventing false
    positives from static timeouts while still catching slow operations.

    Attributes
    ----------
    percentile : float
        Percentile to use for timeout calculation (0.0-1.0).
    min_timeout : float
        Minimum timeout value in seconds.
    max_timeout : float
        Maximum timeout value in seconds.
    window_size : int
        Number of historical measurements to keep.

    Parameters
    ----------
    percentile : float, optional
        Percentile for timeout (by default 0.95 for 95th percentile).
    min_timeout : float, optional
        Minimum timeout in seconds (by default 1.0).
    max_timeout : float, optional
        Maximum timeout in seconds (by default 30.0).
    window_size : int, optional
        Size of rolling window for measurements (by default 100).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> timeout = AdaptiveTimeout(percentile=0.95, min_timeout=0.5, max_timeout=10.0)
    >>> def api_call():
    ...     return "response"
    >>> result = timeout.call(api_call)
    'response'

    >>> # Timeout adapts based on historical latencies
    >>> timeout.current_timeout
    1.0

    Notes
    -----
    The adaptive timeout prevents both false positives (timing out valid slow
    operations) and false negatives (not catching actual slow operations).
    It uses percentile-based calculation for robustness against outliers.

    Complexity
    ----------
    Time: O(n log n) for percentile calculation, Space: O(window_size)
    """

    def __init__(
        self,
        percentile: float = 0.95,
        min_timeout: float = 1.0,
        max_timeout: float = 30.0,
        window_size: int = 100,
    ) -> None:
        """Initialize adaptive timeout with configuration."""
        # Type validation
        if not isinstance(percentile, (int, float)):
            raise TypeError(
                f"percentile must be a number, got {type(percentile).__name__}"
            )
        if not isinstance(min_timeout, (int, float)):
            raise TypeError(
                f"min_timeout must be a number, got {type(min_timeout).__name__}"
            )
        if not isinstance(max_timeout, (int, float)):
            raise TypeError(
                f"max_timeout must be a number, got {type(max_timeout).__name__}"
            )
        if not isinstance(window_size, int):
            raise TypeError(
                f"window_size must be an integer, got {type(window_size).__name__}"
            )

        # Value validation
        if not 0.0 < percentile <= 1.0:
            raise ValueError(f"percentile must be between 0 and 1, got {percentile}")
        if min_timeout <= 0:
            raise ValueError(f"min_timeout must be positive, got {min_timeout}")
        if max_timeout <= 0:
            raise ValueError(f"max_timeout must be positive, got {max_timeout}")
        if min_timeout > max_timeout:
            raise ValueError(
                f"min_timeout ({min_timeout}) must be <= max_timeout ({max_timeout})"
            )
        if window_size <= 0:
            raise ValueError(f"window_size must be positive, got {window_size}")

        self.percentile = percentile
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout
        self.window_size = window_size

        self._latencies: deque[float] = deque(maxlen=window_size)
        self._current_timeout = min_timeout

    def call(self, func: Callable[[], T], *args: Any, **kwargs: Any) -> T:
        """
        Execute function with adaptive timeout.

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
            If execution exceeds current adaptive timeout.
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")

        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time

            # Check if it exceeded current timeout
            if elapsed > self._current_timeout:
                raise TimeoutError(
                    f"Operation took {elapsed:.2f}s, exceeding adaptive timeout "
                    f"of {self._current_timeout:.2f}s"
                )

            # Record successful latency
            self._record_latency(elapsed)
            return result

        except Exception as e:
            elapsed = time.time() - start_time
            # Record latency even on failure for adaptation
            if not isinstance(e, TimeoutError):
                self._record_latency(elapsed)
            raise e

    def _record_latency(self, latency: float) -> None:
        """Record a latency measurement and update timeout."""
        self._latencies.append(latency)
        self._update_timeout()

    def _update_timeout(self) -> None:
        """Recalculate timeout based on historical latencies."""
        if not self._latencies:
            self._current_timeout = self.min_timeout
            return

        # Calculate percentile timeout
        sorted_latencies = sorted(self._latencies)
        index = int(len(sorted_latencies) * self.percentile)
        percentile_value = sorted_latencies[min(index, len(sorted_latencies) - 1)]

        # Clamp to min/max bounds
        self._current_timeout = max(
            self.min_timeout, min(self.max_timeout, percentile_value)
        )

    @property
    def current_timeout(self) -> float:
        """
        Get current adaptive timeout value.

        Returns
        -------
        float
            Current timeout in seconds.

        Examples
        --------
        >>> timeout = AdaptiveTimeout()
        >>> timeout.current_timeout
        1.0
        """
        return self._current_timeout

    @property
    def avg_latency(self) -> float:
        """
        Get average latency from historical measurements.

        Returns
        -------
        float
            Average latency in seconds, or 0.0 if no measurements.

        Examples
        --------
        >>> timeout = AdaptiveTimeout()
        >>> timeout.avg_latency
        0.0
        """
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    def reset(self) -> None:
        """
        Reset historical latencies and timeout to initial state.

        Examples
        --------
        >>> timeout = AdaptiveTimeout()
        >>> timeout.reset()
        >>> len(timeout._latencies)
        0
        """
        self._latencies.clear()
        self._current_timeout = self.min_timeout


def adaptive_timeout(
    func: Callable[[], T],
    percentile: float = 0.95,
    min_timeout: float = 1.0,
    max_timeout: float = 30.0,
) -> T:
    """
    Execute function with one-time adaptive timeout (convenience function).

    Parameters
    ----------
    func : Callable
        Function to execute.
    percentile : float, optional
        Percentile for timeout (by default 0.95).
    min_timeout : float, optional
        Minimum timeout in seconds (by default 1.0).
    max_timeout : float, optional
        Maximum timeout in seconds (by default 30.0).

    Returns
    -------
    T
        Result of the function call.

    Raises
    ------
    TimeoutError
        If execution exceeds timeout.

    Examples
    --------
    >>> def slow_operation():
    ...     return "done"
    >>> result = adaptive_timeout(slow_operation, min_timeout=0.5)
    'done'

    Notes
    -----
    For repeated calls, use AdaptiveTimeout class instance to maintain
    historical latency data.

    Complexity
    ----------
    Time: O(1) for single call, Space: O(1)
    """
    timeout_manager = AdaptiveTimeout(
        percentile=percentile,
        min_timeout=min_timeout,
        max_timeout=max_timeout,
        window_size=1,
    )
    return timeout_manager.call(func)


__all__ = ["AdaptiveTimeout", "adaptive_timeout"]
