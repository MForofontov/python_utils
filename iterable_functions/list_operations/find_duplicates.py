"""
Find duplicate elements in a list with their counts.

This module provides utilities for identifying and counting duplicate elements
in various iterable types.
"""

from collections import Counter
from typing import TypeVar

T = TypeVar("T")


def find_duplicates(items: list[T]) -> dict[T, int]:
    """
    Find duplicate elements in a list and return their counts.

    Parameters
    ----------
    items : list[T]
        The list to analyze for duplicates.

    Returns
    -------
    dict[T, int]
        Dictionary mapping duplicate elements to their occurrence counts.
        Only elements that appear more than once are included.

    Raises
    ------
    TypeError
        If items is not a list.

    Examples
    --------
    >>> find_duplicates([1, 2, 2, 3, 3, 3])
    {2: 2, 3: 3}
    >>> find_duplicates(['a', 'b', 'a'])
    {'a': 2}

    Notes
    -----
    Uses collections.Counter for efficient counting.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items).__name__}")

    counter = Counter(items)
    return {item: count for item, count in counter.items() if count > 1}


__all__ = ["find_duplicates"]
