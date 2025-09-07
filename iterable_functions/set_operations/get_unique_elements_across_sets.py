"""
Get unique elements across sets utilities.

This module provides utilities for getting elements that appear in exactly one set across multiple sets.
"""

from typing import TypeVar, Set, List

T = TypeVar("T")


def get_unique_elements_across_sets(*sets: Set[T]) -> List[T]:
    """
    Get elements that appear in exactly one set across multiple sets.

    This is equivalent to the symmetric difference but returns a list
    instead of a set, preserving some ordering information.

    Parameters
    ----------
    *sets : Set[T]
        Variable number of sets to analyze.

    Returns
    -------
    List[T]
        List of elements that appear in exactly one set.

    Raises
    ------
    TypeError
        If any argument is not a set.
    ValueError
        If fewer than 2 sets are provided.

    Examples
    --------
    >>> set1 = {1, 2, 3}
    >>> set2 = {2, 3, 4}
    >>> set3 = {3, 4, 5}
    >>> get_unique_elements_across_sets(set1, set2, set3)
    [1, 5]

    Notes
    -----
    The order of elements in the result is not guaranteed to be meaningful.

    Complexity
    ----------
    Time: O(n*m), Space: O(m)
    """
    # Input validation
    if len(sets) < 2:
        raise ValueError("At least 2 sets must be provided")

    for i, s in enumerate(sets):
        if not isinstance(s, set):
            raise TypeError(f"All arguments must be sets, got {type(s).__name__} at position {i}")

    # Calculate symmetric difference and convert to list
    symmetric_diff = set_symmetric_difference(*sets)
    return list(symmetric_diff)


def set_symmetric_difference(*sets: Set[T]) -> Set[T]:
    """
    Calculate the symmetric difference of multiple sets.

    The symmetric difference of sets A, B, and C is the set of elements
    that are in exactly one of the sets.

    Parameters
    ----------
    *sets : Set[T]
        Variable number of sets to compute symmetric difference.

    Returns
    -------
    Set[T]
        Symmetric difference of all input sets.

    Raises
    ------
    TypeError
        If any argument is not a set.
    ValueError
        If fewer than 2 sets are provided.

    Examples
    --------
    >>> set1 = {1, 2, 3}
    >>> set2 = {2, 3, 4}
    >>> set3 = {3, 4, 5}
    >>> set_symmetric_difference(set1, set2, set3)
    {1, 5}

    >>> set_symmetric_difference({1, 2}, {2, 3})
    {1, 3}

    >>> set_symmetric_difference({1, 2, 3}, {1, 2, 3})
    set()

    Notes
    -----
    For two sets A and B:
    A △ B = (A - B) ∪ (B - A)

    For multiple sets, the symmetric difference is computed iteratively.

    Complexity
    ----------
    Time: O(n*m) where n is number of sets and m is average set size
    Space: O(m) where m is the size of the result
    """
    # Input validation
    if len(sets) < 2:
        raise ValueError("At least 2 sets must be provided")

    for i, s in enumerate(sets):
        if not isinstance(s, set):
            raise TypeError(f"All arguments must be sets, got {type(s).__name__} at position {i}")

    # Calculate symmetric difference
    if len(sets) == 2:
        # Simple case: symmetric difference of two sets
        return sets[0].symmetric_difference(sets[1])

    # Multiple sets: compute iteratively
    result = sets[0].symmetric_difference(sets[1])
    for s in sets[2:]:
        result = result.symmetric_difference(s)

    return result


__all__ = ['get_unique_elements_across_sets']
