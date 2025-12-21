"""
Get permutations from a set.

This module provides a utility for generating permutations from sets.
"""

import itertools
from typing import TypeVar

T = TypeVar("T")


def get_permutations(input_set: set[T], r: int | None = None) -> list[list[T]]:
    """
    Generate all permutations of r elements from the input set.

    A permutation is an arrangement of items where order matters.

    Parameters
    ----------
    input_set : set[T]
        The input set to generate permutations from.
    r : int | None, optional
        The number of elements in each permutation. If None, uses all elements.

    Returns
    -------
    list[list[T]]
        List of all permutations, sorted lexicographically.

    Raises
    ------
    TypeError
        If input_set is not a set or r is not an int or None.
    ValueError
        If r is negative or larger than the set size.

    Examples
    --------
    >>> s = {1, 2, 3}
    >>> get_permutations(s, 2)
    [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]

    >>> get_permutations(s)  # r=None means all elements
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

    Notes
    -----
    Unlike combinations, permutations consider order.
    For large sets, this can generate many results.

    Complexity
    ----------
    Time: O(P(n,r) * r * log P(n,r)), Space: O(P(n,r) * r)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if r is None:
        r = len(input_set)
    elif not isinstance(r, int):
        raise TypeError(f"r must be an int or None, got {type(r).__name__}")

    if r < 0:
        raise ValueError(f"r must be non-negative, got {r}")

    if r > len(input_set):
        raise ValueError(f"r cannot be larger than set size {len(input_set)}, got {r}")

    # Handle edge cases
    if r == 0:
        return [[]]

    if not input_set:
        return []

    # Generate permutations
    elements = sorted(list(input_set))  # type: ignore[type-var]
    permutations = [list(perm) for perm in itertools.permutations(elements, r)]
    permutations.sort()  # Ensure lexicographic ordering

    return permutations


__all__ = ["get_permutations"]
