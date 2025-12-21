"""Set partition utilities."""

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def partition_set_by_predicate(
    input_set: set[T], predicate: Callable[[T], bool]
) -> tuple[set[T], set[T]]:
    """
    Partition a set into two subsets based on a predicate function.

    Elements for which the predicate returns True go into the first set,
    elements for which it returns False go into the second set.

    Parameters
    ----------
    input_set : set[T]
        The input set to partition.
    predicate : callable
        Function that takes an element and returns True or False.

    Returns
    -------
    tuple[set[T], set[T]]
        Tuple of (true_set, false_set) where true_set contains elements
        where predicate(element) is True, and false_set contains elements
        where predicate(element) is False.

    Raises
    ------
    TypeError
        If input_set is not a set or predicate is not callable.

    Examples
    --------
    >>> numbers = {1, 2, 3, 4, 5, 6}
    >>> even, odd = partition_set_by_predicate(numbers, lambda x: x % 2 == 0)
    >>> even
    {2, 4, 6}
    >>> odd
    {1, 3, 5}

    >>> strings = {'apple', 'banana', 'cherry', 'date'}
    >>> long, short = partition_set_by_predicate(strings, lambda s: len(s) > 5)
    >>> long
    {'banana', 'cherry'}
    >>> short
    {'apple', 'date'}

    Notes
    -----
    The original set is partitioned into two disjoint subsets whose union
    equals the original set.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    # Input validation
    if not isinstance(input_set, set):
        raise TypeError(f"input_set must be a set, got {type(input_set).__name__}")

    if not callable(predicate):
        raise TypeError(f"predicate must be callable, got {type(predicate).__name__}")

    # Partition the set
    true_set = set()
    false_set = set()

    for element in input_set:
        if predicate(element):
            true_set.add(element)
        else:
            false_set.add(element)

    return true_set, false_set


__all__ = ["partition_set_by_predicate"]
