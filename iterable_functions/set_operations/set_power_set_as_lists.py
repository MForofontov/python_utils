"""
Set power set as lists utilities.

This module provides utilities for generating power sets of sets as lists.
"""

from typing import TypeVar

T = TypeVar("T")


def set_power_set_as_lists(input_set: set[T]) -> list[list[T]]:
    """
    Generate the power set of a given set, returning lists instead of frozensets.

    This returns lists for easier manipulation.

    Parameters
    ----------
    input_set : set[T]
        The input set to generate power set for.

    Returns
    -------
    list[list[T]]
        Power set as a list of lists, sorted by subset size and
        lexicographically.

    Raises
    ------
    TypeError
        If input_set is not a set.

    Examples
    --------
    >>> s = {1, 2}
    >>> power_set = set_power_set_as_lists(s)
    >>> power_set
    [[], [1], [2], [1, 2]]

    >>> set_power_set_as_lists({3, 1, 2})
    [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]

    Notes
    -----
    The result is sorted first by subset size, then lexicographically within each size.

    Complexity
    ----------
    Time: O(2^n * n * log(2^n)), Space: O(2^n * n)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    # Convert to list for indexing
    elements = list(input_set)
    try:
        elements = sorted(elements)
    except TypeError:
        pass  # If elements are not comparable, skip sorting
    n = len(elements)

    # Generate all possible subsets
    subsets = []

    for i in range(2**n):
        subset = []
        for j in range(n):
            if i & (1 << j):
                subset.append(elements[j])
        subsets.append(subset)

    # Try to sort by length and lexicographically, skip if not possible
    try:
        subsets.sort(key=lambda x: (len(x), x))
    except TypeError:
        subsets.sort(key=lambda x: len(x))

    return subsets


__all__ = ["set_power_set_as_lists"]
