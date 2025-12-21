"""
Partition set into n parts utilities.

This module provides utilities for partitioning sets into n approximately equal-sized subsets.
"""

from typing import TypeVar

T = TypeVar("T")


def partition_set_into_n_parts(input_set: set[T], n: int) -> list[set[T]]:
    """
    Partition a set into n approximately equal-sized subsets.

    This distributes elements as evenly as possible across n subsets.

    Parameters
    ----------
    input_set : set[T]
        The input set to partition.
    n : int
        Number of partitions to create.

    Returns
    -------
    list[set[T]]
        List of n subsets. The union of all subsets equals the input set,
        and all subsets are pairwise disjoint.

    Raises
    ------
    TypeError
        If input_set is not a set or n is not an int.
    ValueError
        If n is less than 1.

    Examples
    --------
    >>> numbers = {1, 2, 3, 4, 5, 6, 7}
    >>> partitions = partition_set_into_n_parts(numbers, 3)
    >>> len(partitions)
    3
    >>> sum(len(p) for p in partitions) == len(numbers)
    True

    >>> # Check that partitions are disjoint
    >>> all(len(p1 & p2) == 0 for i, p1 in enumerate(partitions)
    ...     for p2 in partitions[i+1:])
    True

    Notes
    -----
    Elements are distributed round-robin fashion to ensure approximately
    equal sizes. The order of elements in each partition is not guaranteed.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if type(n) is not int:
        raise TypeError(f"n must be an int, got {type(n).__name__}")

    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")

    # Handle edge cases
    if n >= len(input_set):
        # More partitions than elements
        partitions: list[set[T]] = [set() for _ in range(n)]
        for i, element in enumerate(input_set):
            if i < n:
                partitions[i].add(element)
        return partitions

    # Convert to list for indexing
    elements = list(input_set)

    # Create partitions
    partitions = [set() for _ in range(n)]

    # Distribute elements round-robin
    for i, element in enumerate(elements):
        partition_index = i % n
        partitions[partition_index].add(element)

    return partitions


__all__ = ["partition_set_into_n_parts"]
