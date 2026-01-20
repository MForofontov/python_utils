"""
Create rate limiter object.
"""

import time


class RateLimiter:
    """Rate limiter using token bucket algorithm."""

    def __init__(self, calls_per_second: float) -> None:
        """
        Initialize rate limiter.

        Parameters
        ----------
        calls_per_second : float
            Maximum calls per second.
        """
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_called = 0.0

    def wait(self) -> None:
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_called
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_called = time.time()


def create_rate_limiter(
    calls_per_second: float = 1.0,
) -> RateLimiter:
    """
    Create a rate limiter object.

    Parameters
    ----------
    calls_per_second : float, optional
        Maximum calls per second (by default 1.0).

    Returns
    -------
    RateLimiter
        Rate limiter object with wait() method.

    Raises
    ------
    TypeError
        If calls_per_second is not a number.
    ValueError
        If calls_per_second is non-positive.

    Examples
    --------
    >>> limiter = create_rate_limiter(calls_per_second=2.0)
    >>> limiter.wait()  # Waits if necessary
    >>> # Make rate-limited call
    >>> limiter.wait()  # Waits again

    Notes
    -----
    Use wait() method before each operation to enforce rate limit.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(calls_per_second, (int, float)):
        raise TypeError(
            f"calls_per_second must be a number, got {type(calls_per_second).__name__}"
        )

    if calls_per_second <= 0:
        raise ValueError(f"calls_per_second must be positive, got {calls_per_second}")

    return RateLimiter(calls_per_second)


__all__ = ["create_rate_limiter", "RateLimiter"]
