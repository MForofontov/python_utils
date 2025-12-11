"""
Benchmark function execution time.
"""

import time
from typing import Any
from collections.abc import Callable


def benchmark_function(
    func: Callable[..., Any],
    *args: Any,
    iterations: int = 1000,
    **kwargs: Any,
) -> dict[str, float]:
    """
    Benchmark a function's execution time.

    Parameters
    ----------
    func : Callable[..., Any]
        Function to benchmark.
    *args : Any
        Positional arguments for func.
    iterations : int, optional
        Number of iterations to run (by default 1000).
    **kwargs : Any
        Keyword arguments for func.

    Returns
    -------
    dict[str, float]
        Dictionary containing 'total_time', 'avg_time', 'min_time', 'max_time'.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If iterations is non-positive.

    Examples
    --------
    >>> def test_func(x):
    ...     return x * 2
    >>> result = benchmark_function(test_func, 5, iterations=100)
    >>> 'avg_time' in result
    True

    Complexity
    ----------
    Time: O(n * f), Space: O(n), where n is iterations and f is function complexity
    """
    if not callable(func):
        raise TypeError(f"func must be callable, got {type(func).__name__}")
    if not isinstance(iterations, int):
        raise TypeError(f"iterations must be an integer, got {type(iterations).__name__}")
    
    if iterations <= 0:
        raise ValueError(f"iterations must be positive, got {iterations}")
    
    times = []
    
    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    return {
        'total_time': sum(times),
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
    }


__all__ = ['benchmark_function']
