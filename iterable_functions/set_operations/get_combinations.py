"""
Get combinations from a set.

This module provides a utility for generating combinations from sets.
"""

from typing import TypeVar
import itertools

T = TypeVar("T")


def get_combinations(input_set: set[T], r: int) -> list[list[T]]:
    """
    Generate all combinations of r elements from the input set.

    A combination is a selection of items from the set where order doesn't matter.

    Parameters
    ----------
    input_set : Set[T]
        The input set to generate combinations from.
    r : int
        The number of elements in each combination.

    Returns
    -------
    List[List[T]]
        List of all combinations, where each combination is a sorted list.

    Raises
    ------
    TypeError
        If input_set is not a set or r is not an int.
    ValueError
        If r is negative or larger than the set size.

    Examples
    --------
    >>> s = {1, 2, 3, 4}
    >>> get_combinations(s, 2)
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

    >>> get_combinations(s, 3)
    [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]

    >>> get_combinations(s, 0)
    [[]]

    >>> get_combinations(s, 4)
    [[1, 2, 3, 4]]

    Notes
    -----
    Combinations are returned in lexicographic order.
    This is equivalent to itertools.combinations but works with sets.

    Complexity
    ----------
    Time: O(C(n,r) * r * log C(n,r)), Space: O(C(n,r) * r)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if not isinstance(r, int):
        raise TypeError(f"r must be an int, got {type(r).__name__}")

    if r < 0:
        raise ValueError(f"r must be non-negative, got {r}")

    if r > len(input_set):
        raise ValueError(f"r cannot be larger than set size {len(input_set)}, got {r}")

    # Handle edge cases
    if r == 0:
        return [[]]

    # Generate combinations
    elements = sorted(list(input_set))
    combinations = [list(comb) for comb in itertools.combinations(elements, r)]
    combinations.sort()  # Ensure lexicographic ordering

    return combinations


__all__ = ['get_combinations']
