"""
Group list elements by a key function.

This module provides functionality to group elements of a list based on a key function.
"""

from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")
K = TypeVar("K")


def group_by(
    items: list[T],
    key_func: Callable[[T], K] | None = None,
) -> dict[K, list[T]]:
    """
    Group list elements by a key function.

    Parameters
    ----------
    items : list[T]
        The list of items to group.
    key_func : Callable[[T], K] | None, optional
        Function to extract the grouping key from each item.
        If None, uses the item itself as the key (by default None).

    Returns
    -------
    dict[K, list[T]]
        Dictionary where keys are the grouping values and values are lists of items.

    Raises
    ------
    TypeError
        If items is not a list or key_func is not callable.

    Examples
    --------
    >>> # Group by length
    >>> words = ['cat', 'dog', 'bird', 'elephant']
    >>> group_by(words, lambda x: len(x))
    {3: ['cat', 'dog'], 4: ['bird'], 8: ['elephant']}

    >>> # Group by first letter
    >>> group_by(words, lambda x: x[0])
    {'c': ['cat'], 'd': ['dog'], 'b': ['bird'], 'e': ['elephant']}

    >>> # Group numbers by parity
    >>> numbers = [1, 2, 3, 4, 5, 6]
    >>> group_by(numbers, lambda x: 'even' if x % 2 == 0 else 'odd')
    {'odd': [1, 3, 5], 'even': [2, 4, 6]}

    >>> # Group without key function (uses items as keys)
    >>> items = ['a', 'b', 'a', 'c', 'b']
    >>> group_by(items)
    {'a': ['a', 'a'], 'b': ['b', 'b'], 'c': ['c']}

    Notes
    -----
    The function preserves the original order of items within each group.
    If key_func is None, each item becomes its own key, effectively grouping duplicates.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    # Input validation
    if not isinstance(items, list):
        raise TypeError(f"items must be a list, got {type(items).__name__}")

    if key_func is not None and not callable(key_func):
        raise TypeError(
            f"key_func must be callable or None, got {type(key_func).__name__}"
        )

    # Group items
    result: dict[K, list[T]] = {}

    for item in items:
        if key_func is None:
            # Use item itself as key (for grouping duplicates)
            key = item  # type: ignore
        else:
            key = key_func(item)

        if key not in result:
            result[key] = []
        result[key].append(item)

    return result


__all__ = ["group_by"]
