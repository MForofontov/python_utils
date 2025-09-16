"""
Set cartesian product utilities.

This module provides utilities for computing cartesian products of sets.
"""

import itertools
from typing import TypeVar

T = TypeVar("T")


def set_cartesian_product(*sets: set[T]) -> set[tuple[T, ...]]:
    """
    Calculate the cartesian product of multiple sets.

    The cartesian product of sets A, B, and C is the set of all possible
    ordered tuples where the first element is from A, the second from B, etc.

    Parameters
    ----------
    *sets : set[T]
        Variable number of sets to compute cartesian product.

    Returns
    -------
    set[tuple[T, ...]]
        Set of tuples representing the cartesian product.

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
    >>> set_cartesian_product(set1, set2)
    {(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')}

    >>> set3 = {'x', 'y'}
    >>> set_cartesian_product(set1, set2, set3)
    {(1, 'a', 'x'), (1, 'a', 'y'), (1, 'b', 'x'), (1, 'b', 'y'),
     (2, 'a', 'x'), (2, 'a', 'y'), (2, 'b', 'x'), (2, 'b', 'y')}

    >>> set_cartesian_product({1})
    {(1,)}

    Notes
    -----
    For sets A and B:
    A × B = {(a, b) | a ∈ A, b ∈ B}

    The result contains tuples in lexicographic order.

    Complexity
    ----------
    Time: O(prod(|S_i| for S_i in sets)), Space: O(prod(|S_i| for S_i in sets))
    """
    # Input validation
    if len(sets) == 0:
        raise ValueError("At least one set must be provided")

    for i, s in enumerate(sets):
        if not isinstance(s, set):
            raise TypeError(
                f"All arguments must be sets, got {type(s).__name__} at position {i}"
            )

    # Calculate cartesian product
    if len(sets) == 1:
        # Single set case
        return {(item,) for item in sets[0]}

    # Multiple sets case
    product = itertools.product(*sets)
    return set(product)


__all__ = ["set_cartesian_product"]
