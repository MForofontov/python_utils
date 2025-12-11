"""
Rate-limited scraper decorator.
"""

import time
from collections.abc import Callable
from functools import wraps
from typing import TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def rate_limited_scraper(
    calls_per_second: float = 1.0,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to rate-limit scraping function calls.

    Parameters
    ----------
    calls_per_second : float, optional
        Maximum calls per second (by default 1.0).

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        Decorated function with rate limiting.

    Raises
    ------
    TypeError
        If calls_per_second is not a number.
    ValueError
        If calls_per_second is non-positive.

    Examples
    --------
    >>> @rate_limited_scraper(calls_per_second=2.0)
    ... def fetch_url(url):
    ...     return f"Fetched {url}"
    >>> result = fetch_url("https://example.com")
    >>> result
    'Fetched https://example.com'

    Notes
    -----
    Uses time.sleep to enforce rate limiting between calls.

    Complexity
    ----------
    Time: O(1) + function time, Space: O(1)
    """
    if not isinstance(calls_per_second, (int, float)):
        raise TypeError(
            f"calls_per_second must be a number, got {type(calls_per_second).__name__}"
        )
    
    if calls_per_second <= 0:
        raise ValueError(f"calls_per_second must be positive, got {calls_per_second}")
    
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]  # Use list to allow modification in closure
    
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            
            last_called[0] = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


__all__ = ['rate_limited_scraper']
