"""
Circuit breaker pattern implementation to prevent cascading failures.
"""

import time
from collections.abc import Callable
from enum import Enum
from typing import Any, TypeVar

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker pattern to prevent cascading failures.

    The circuit breaker monitors for failures and prevents the application from
    repeatedly trying to execute an operation that's likely to fail. It has three states:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, requests are immediately rejected
    - HALF_OPEN: Testing if the service has recovered

    Attributes
    ----------
    failure_threshold : int
        Number of failures before opening the circuit.
    recovery_timeout : float
        Time in seconds before attempting to close the circuit.
    success_threshold : int
        Number of successes in HALF_OPEN state to close the circuit.
    state : CircuitState
        Current state of the circuit breaker.

    Parameters
    ----------
    failure_threshold : int, optional
        Number of consecutive failures to open circuit (by default 5).
    recovery_timeout : float, optional
        Seconds to wait before trying again (by default 60.0).
    success_threshold : int, optional
        Successes needed in HALF_OPEN to close circuit (by default 2).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.

    Examples
    --------
    >>> cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)
    >>> def risky_operation():
    ...     # Your code here
    ...     return "success"
    >>> result = cb.call(risky_operation)
    'success'

    >>> # After 3 failures, circuit opens
    >>> cb.state == CircuitState.OPEN
    True

    Notes
    -----
    The circuit breaker prevents cascading failures by failing fast when
    a service is unavailable, giving it time to recover.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        success_threshold: int = 2,
    ) -> None:
        """Initialize circuit breaker with thresholds."""
        # Type validation
        if not isinstance(failure_threshold, int):
            raise TypeError(
                f"failure_threshold must be an integer, got {type(failure_threshold).__name__}"
            )
        if not isinstance(recovery_timeout, (int, float)):
            raise TypeError(
                f"recovery_timeout must be a number, got {type(recovery_timeout).__name__}"
            )
        if not isinstance(success_threshold, int):
            raise TypeError(
                f"success_threshold must be an integer, got {type(success_threshold).__name__}"
            )

        # Value validation
        if failure_threshold <= 0:
            raise ValueError(
                f"failure_threshold must be positive, got {failure_threshold}"
            )
        if recovery_timeout <= 0:
            raise ValueError(
                f"recovery_timeout must be positive, got {recovery_timeout}"
            )
        if success_threshold <= 0:
            raise ValueError(
                f"success_threshold must be positive, got {success_threshold}"
            )

        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: float | None = None

    def call(self, func: Callable[[], T], *args: Any, **kwargs: Any) -> T:
        """
        Execute function through the circuit breaker.

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
        Exception
            If circuit is OPEN or function execution fails.
        """
        if not callable(func):
            raise TypeError(f"func must be callable, got {type(func).__name__}")

        # Check if we should transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception(
                    f"Circuit breaker is OPEN. Service unavailable. "
                    f"Retry after {self.recovery_timeout}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _on_success(self) -> None:
        """Handle successful execution."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._close_circuit()
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def _on_failure(self) -> None:
        """Handle failed execution."""
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self._open_circuit()
        elif self.state == CircuitState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self._open_circuit()

    def _open_circuit(self) -> None:
        """Transition to OPEN state."""
        self.state = CircuitState.OPEN
        self.failure_count = 0
        self.success_count = 0

    def _close_circuit(self) -> None:
        """Transition to CLOSED state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0

    def reset(self) -> None:
        """
        Manually reset the circuit breaker to CLOSED state.

        Examples
        --------
        >>> cb = CircuitBreaker()
        >>> cb.reset()
        >>> cb.state == CircuitState.CLOSED
        True
        """
        self._close_circuit()
        self.last_failure_time = None


__all__ = ["CircuitBreaker", "CircuitState"]
