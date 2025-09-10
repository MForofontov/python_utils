"""
Get set partitions utilities.

This module provides utilities for generating all possible ways to partition a set into k non-empty subsets.
"""

from typing import TypeVar

T = TypeVar("T")


def get_set_partitions(input_set: set[T], k: int) -> list[list[set[T]]]:
    """
    Generate all possible ways to partition a set into k non-empty subsets.

    This generates all distinct partitions of the set into exactly k subsets.
    Note: This can be computationally expensive for large sets.

    Parameters
    ----------
    input_set : set[T]
        The input set to partition.
    k : int
        Number of subsets to partition into.

    Returns
    -------
    list[list[set[T]]]
        List of all possible partitions, where each partition is a list of
        ``k`` subsets.

    Raises
    ------
    TypeError
        If input_set is not a set or k is not an int.
    ValueError
        If k is less than 1 or greater than the set size.

    Examples
    --------
    >>> s = {1, 2, 3}
    >>> partitions = get_set_partitions(s, 2)
    >>> len(partitions)  # Number of ways to partition into 2 subsets
    3

    >>> # One possible partition: [{1}, {2, 3}]
    >>> # Another: [{2}, {1, 3}]
    >>> # Another: [{3}, {1, 2}]

    Notes
    -----
    This uses a recursive algorithm to generate all partitions.
    For large sets, this can be very slow due to combinatorial explosion.

    Complexity
    ----------
    Time: O(k! * Stirling2nd(n,k)), Space: O(k! * Stirling2nd(n,k) * n)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if not isinstance(k, int):
        raise TypeError(f"k must be an int, got {type(k).__name__}")

    if k < 1:
        raise ValueError(f"k must be at least 1, got {k}")

    if k > len(input_set):
        raise ValueError(f"k cannot be greater than set size {len(input_set)}, got {k}")

    # Convert to sorted list for consistent ordering
    elements = sorted(list(input_set))

    def generate_partitions(remaining: list[T], num_parts: int) -> list[list[list[T]]]:
        """Recursive helper to generate partitions."""
        if num_parts == 1:
            return [[remaining]]

        if not remaining:
            return []

        result = []
        first = remaining[0]
        rest = remaining[1:]

        # Try putting first element in each possible subset
        for i in range(num_parts):
            # Get partitions of the rest
            sub_partitions = generate_partitions(rest, num_parts if i == num_parts - 1 else num_parts - 1)

            for partition in sub_partitions:
                # Insert first element into the i-th subset
                new_partition = partition.copy()
                if i < len(new_partition):
                    new_partition[i] = [first] + new_partition[i]
                else:
                    new_partition.append([first])
                result.append(new_partition)

        return result

    # Generate partitions and convert to sets
    raw_partitions = generate_partitions(elements, k)
    set_partitions = []

    for partition in raw_partitions:
        set_partition = [set(subset) for subset in partition]
        set_partitions.append(set_partition)

    # Remove duplicates (since we're dealing with sets)
    unique_partitions = []
    seen = set()

    for partition in set_partitions:
        # Create a frozenset of frozensets for hashing
        partition_hash = frozenset(frozenset(s) for s in partition)
        if partition_hash not in seen:
            seen.add(partition_hash)
            unique_partitions.append(partition)

    return unique_partitions


__all__ = ['get_set_partitions']
