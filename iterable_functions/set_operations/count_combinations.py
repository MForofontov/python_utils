"""
Count combinations from a set.

This module provides a utility for counting combinations from sets.
"""

from typing import TypeVar

T = TypeVar("T")


def count_combinations(input_set: set[T], r: int) -> int:
    """
    Count the number of combinations of r elements from the input set.

    This is more efficient than generating all combinations when you only
    need the count.

    Parameters
    ----------
    input_set : Set[T]
        The input set.
    r : int
        The number of elements in each combination.

    Returns
    -------
    int
        Number of combinations.

    Raises
    ------
    TypeError
        If input_set is not a set or r is not an int.
    ValueError
        If r is negative or larger than the set size.

    Examples
    --------
    >>> s = {1, 2, 3, 4, 5}
    >>> count_combinations(s, 2)
    10

    >>> count_combinations(s, 3)
    10

    >>> count_combinations(s, 0)
    1

    Notes
    -----
    This uses the mathematical formula C(n,r) = n! / (r! * (n-r)!)

    Complexity
    ----------
    Time: O(min(r, n-r)), Space: O(1)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if not isinstance(r, int):
        raise TypeError(f"r must be an int, got {type(r).__name__}")

    if r < 0:
        raise ValueError(f"r must be non-negative, got {r}")

    n = len(input_set)
    if r > n:
        raise ValueError(f"r cannot be larger than set size {n}, got {r}")

    # Handle edge cases
    if r == 0 or r == n:
        return 1

    # Calculate C(n,r) efficiently to avoid overflow
    if r > n - r:
        r = n - r

    result = 1
    for i in range(1, r + 1):
        result = result * (n - r + i) // i

    return result


__all__ = ['count_combinations']
