"""
Create sliding windows from a list.

This module provides utilities for creating sliding windows of specified size.
"""

from typing import TypeVar
from collections.abc import Iterator

T = TypeVar("T")


def sliding_window(items: list[T], window_size: int) -> Iterator[list[T]]:
    """
    Create sliding windows of specified size from a list.

    Parameters
    ----------
    items : list[T]
        The list to create windows from.
    window_size : int
        The size of each window.

    Yields
    ------
    list[T]
        Sliding windows of the specified size.

    Raises
    ------
    TypeError
        If items is not a list or window_size is not an int.
    ValueError
        If window_size is less than 1.

    Examples
    --------
    >>> list(sliding_window([1, 2, 3, 4, 5], 3))
    [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
    >>> list(sliding_window(['a', 'b', 'c'], 2))
    [['a', 'b'], ['b', 'c']]

    Complexity
    ----------
    Time: O(n), Space: O(window_size)
    """
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items).__name__}")
    if not isinstance(window_size, int):
        raise TypeError(f"window_size must be an int, got {type(window_size).__name__}")
    if window_size < 1:
        raise ValueError(f"window_size must be at least 1, got {window_size}")

    for i in range(len(items) - window_size + 1):
        yield items[i:i + window_size]


__all__ = ['sliding_window']
