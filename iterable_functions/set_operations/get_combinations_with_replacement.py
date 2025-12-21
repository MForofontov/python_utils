"""
Get combinations with replacement from a set.

This module provides a utility for generating combinations with replacement from sets.
"""

import itertools
from typing import TypeVar

T = TypeVar("T")


def get_combinations_with_replacement(input_set: set[T], r: int) -> list[list[T]]:
    """
    Generate all combinations with replacement of r elements from the input set.

    Each element can be selected multiple times, but order doesn't matter.

    Parameters
    ----------
    input_set : set[T]
        The input set to generate combinations from.
    r : int
        The number of elements in each combination.

    Returns
    -------
    list[list[T]]
        List of all combinations with replacement, sorted lexicographically.

    Raises
    ------
    TypeError
        If input_set is not a set or r is not an int.
    ValueError
        If r is negative.

    Examples
    --------
    >>> s = {1, 2, 3}
    >>> get_combinations_with_replacement(s, 2)
    [[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]

    >>> get_combinations_with_replacement(s, 3)
    [[1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 2, 2], [1, 2, 3],
     [1, 3, 3], [2, 2, 2], [2, 2, 3], [2, 3, 3], [3, 3, 3]]

    Notes
    -----
    This allows the same element to be selected multiple times.
    Results are sorted lexicographically.

    Complexity
    ----------
    Time: O(C(n+r-1,r) * r * log C(n+r-1,r)), Space: O(C(n+r-1,r) * r)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if not isinstance(r, int):
        raise TypeError(f"r must be an int, got {type(r).__name__}")

    if r < 0:
        raise ValueError(f"r must be non-negative, got {r}")

    # Handle edge cases
    if r == 0:
        return [[]]

    if not input_set:
        return []

    # Generate combinations with replacement
    elements = sorted(list(input_set))  # type: ignore[type-var]
    combinations = [
        list(comb) for comb in itertools.combinations_with_replacement(elements, r)
    ]
    combinations.sort()  # Ensure lexicographic ordering

    return combinations


__all__ = ["get_combinations_with_replacement"]
