"""
Get subsets of specific size utilities.

This module provides utilities for getting subsets of a specific size from sets.
"""

from typing import TypeVar

T = TypeVar("T")


def get_subsets_of_size(input_set: set[T], size: int) -> list[list[T]]:
    """
    Get all subsets of a specific size from the input set.

    Parameters
    ----------
    input_set : set[T]
        The input set to generate subsets from.
    size : int
        The desired size of subsets.

    Returns
    -------
    list[List[T]]
        List of subsets of the specified size, sorted lexicographically.

    Raises
    ------
    TypeError
        If input_set is not a set or size is not an int.
    ValueError
        If size is negative or larger than the set size.

    Examples
    --------
    >>> s = {1, 2, 3, 4}
    >>> get_subsets_of_size(s, 2)
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

    >>> get_subsets_of_size(s, 0)
    [[]]

    >>> get_subsets_of_size(s, 4)
    [[1, 2, 3, 4]]

    Notes
    -----
    This uses combinations to generate subsets of exact size.

    Complexity
    ----------
    Time: O(C(n,k) * k * log C(n,k)), Space: O(C(n,k) * k)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if not isinstance(size, int):
        raise TypeError(f"size must be an int, got {type(size).__name__}")

    if size < 0:
        raise ValueError(f"size must be non-negative, got {size}")

    if size > len(input_set):
        raise ValueError(f"size cannot be larger than set size {len(input_set)}, got {size}")

    # Handle edge cases
    if size == 0:
        return [[]]

    # Generate combinations
    from itertools import combinations
    elements = sorted(list(input_set))
    subsets = [list(comb) for comb in combinations(elements, size)]
    subsets.sort()  # Ensure lexicographic ordering

    return subsets


__all__ = ['get_subsets_of_size']
