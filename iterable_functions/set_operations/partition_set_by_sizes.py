"""
Partition a set into subsets of given sizes.

This module provides utilities for partitioning sets into smaller subsets.
"""

from typing import TypeVar, Any, Set, List

T = TypeVar("T")


def partition_set_by_sizes(input_set: Set[T], sizes: List[int]) -> List[Set[T]]:
    """
    Partition a set into subsets of specified sizes.

    Parameters
    ----------
    input_set : Set[T]
        The set to partition.
    sizes : List[int]
        List of subset sizes. Sum must equal len(input_set).

    Returns
    -------
    List[Set[T]]
        List of subsets with the specified sizes.

    Raises
    ------
    TypeError
        If input_set is not a set or sizes is not a list.
    ValueError
        If sizes don't sum to len(input_set) or contain invalid values.

    Examples
    --------
    >>> partition_set_by_sizes({1, 2, 3, 4, 5}, [2, 3])
    [{1, 2}, {3, 4, 5}]
    >>> partition_set_by_sizes({'a', 'b', 'c'}, [1, 1, 1])
    [{'a'}, {'b'}, {'c'}]

    Notes
    -----
    The partitioning is deterministic but order-dependent on set iteration.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")
    if not isinstance(sizes, list):
        raise TypeError(f"sizes must be a list, got {type(sizes).__name__}")

    # Validate sizes
    if not all(isinstance(size, int) for size in sizes):
        raise TypeError("All sizes must be integers")
    if not all(size > 0 for size in sizes):
        raise ValueError("All sizes must be positive")
    if sum(sizes) != len(input_set):
        raise ValueError(f"Sum of sizes ({sum(sizes)}) must equal set size ({len(input_set)})")

    result = []
    items_list = list(input_set)
    start_idx = 0

    for size in sizes:
        subset = set(items_list[start_idx:start_idx + size])
        result.append(subset)
        start_idx += size

    return result


__all__ = ['partition_set_by_sizes']
