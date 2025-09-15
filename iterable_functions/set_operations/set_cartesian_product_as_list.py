"""
Set cartesian product as list utilities.

This module provides utilities for computing cartesian products of sets as lists.
"""

from typing import TypeVar
import itertools

T = TypeVar("T")


def set_cartesian_product_as_list(*sets: set[T]) -> list[tuple[T, ...]]:
    """
    Calculate the cartesian product of multiple sets, returning a list.

    This returns a list instead of a set, which may be more convenient
    for iteration and preserves order.

    Parameters
    ----------
    *sets : set[T]
        Variable number of sets to compute cartesian product.

    Returns
    -------
    list[tuple[T, ...]]
        List of tuples representing the cartesian product.

    Raises
    ------
    TypeError
        If any argument is not a set.
    ValueError
        If no sets are provided.

    Examples
    --------
    >>> set1 = {1, 2}
    >>> set2 = {'a', 'b'}
    >>> set_cartesian_product_as_list(set1, set2)
    [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

    Notes
    -----
    The result is sorted lexicographically for consistent ordering.

    Complexity
    ----------
    Time: O(prod(|S_i| for S_i in sets) * log(prod)), Space: O(prod(|S_i| for S_i in sets))
    """
    # Input validation
    if len(sets) == 0:
        raise ValueError("At least one set must be provided")

    for i, s in enumerate(sets):
        if not isinstance(s, set):
            raise TypeError(
                f"All arguments must be sets, got {type(s).__name__} at position {i}"
            )

    # Calculate cartesian product and sort for consistent ordering
    product = list(itertools.product(*sets))
    product.sort()
    return product


__all__ = ["set_cartesian_product_as_list"]
