"""
Compare performance of two functions.
"""

from collections.abc import Callable
from typing import Any

from .benchmark_function import benchmark_function


def compare_functions(
    func1: Callable[..., Any],
    func2: Callable[..., Any],
    args1: tuple[Any, ...] = (),
    args2: tuple[Any, ...] = (),
    iterations: int = 1000,
) -> dict[str, Any]:
    """
    Compare performance of two functions.

    Parameters
    ----------
    func1 : Callable[..., Any]
        First function to benchmark.
    func2 : Callable[..., Any]
        Second function to benchmark.
    args1 : tuple[Any, ...], optional
        Arguments for func1 (by default ()).
    args2 : tuple[Any, ...], optional
        Arguments for func2 (by default ()).
    iterations : int, optional
        Number of iterations (by default 1000).

    Returns
    -------
    dict[str, Any]
        Dictionary containing benchmark results for both functions and comparison.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If iterations is non-positive.

    Examples
    --------
    >>> def func_a(x):
    ...     return x * 2
    >>> def func_b(x):
    ...     return x + x
    >>> result = compare_functions(func_a, func_b, (5,), (5,), iterations=100)
    >>> 'func1_avg_time' in result
    True

    Complexity
    ----------
    Time: O(n * (f1 + f2)), Space: O(n)
    """
    if not callable(func1):
        raise TypeError(f"func1 must be callable, got {type(func1).__name__}")
    if not callable(func2):
        raise TypeError(f"func2 must be callable, got {type(func2).__name__}")
    if not isinstance(args1, tuple):
        raise TypeError(f"args1 must be a tuple, got {type(args1).__name__}")
    if not isinstance(args2, tuple):
        raise TypeError(f"args2 must be a tuple, got {type(args2).__name__}")
    if not isinstance(iterations, int):
        raise TypeError(
            f"iterations must be an integer, got {type(iterations).__name__}"
        )

    if iterations <= 0:
        raise ValueError(f"iterations must be positive, got {iterations}")

    result1 = benchmark_function(func1, *args1, iterations=iterations)
    result2 = benchmark_function(func2, *args2, iterations=iterations)

    speedup = (
        result2["avg_time"] / result1["avg_time"]
        if result1["avg_time"] > 0
        else float("inf")
    )

    return {
        "func1_avg_time": result1["avg_time"],
        "func1_total_time": result1["total_time"],
        "func2_avg_time": result2["avg_time"],
        "func2_total_time": result2["total_time"],
        "speedup": speedup,
        "faster_function": "func1"
        if result1["avg_time"] < result2["avg_time"]
        else "func2",
    }


__all__ = ["compare_functions"]
