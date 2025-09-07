"""
Find differences between dictionaries.

This module provides utilities for computing differences between dictionaries.
"""

from typing import TypeVar, Any, Dict, Set, Tuple

K = TypeVar("K")
V = TypeVar("V")


def dict_difference(
    dict1: Dict[K, V],
    dict2: Dict[K, V]
) -> Tuple[Set[K], Set[K], Dict[K, Tuple[V, V]]]:
    """
    Find differences between two dictionaries.

    Parameters
    ----------
    dict1 : Dict[K, V]
        First dictionary.
    dict2 : Dict[K, V]
        Second dictionary.

    Returns
    -------
    Tuple[Set[K], Set[K], Dict[K, Tuple[V, V]]]
        A tuple containing:
        - Keys only in dict1
        - Keys only in dict2
        - Keys in both with different values (old_value, new_value)

    Raises
    ------
    TypeError
        If either input is not a dictionary.

    Examples
    --------
    >>> d1 = {'a': 1, 'b': 2, 'c': 3}
    >>> d2 = {'b': 2, 'c': 4, 'd': 5}
    >>> only_in_1, only_in_2, different = dict_difference(d1, d2)
    >>> only_in_1
    {'a'}
    >>> only_in_2
    {'d'}
    >>> different
    {'c': (3, 4)}

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(dict1, dict):
        raise TypeError(f"dict1 must be a dict, got {type(dict1).__name__}")
    if not isinstance(dict2, dict):
        raise TypeError(f"dict2 must be a dict, got {type(dict2).__name__}")

    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    only_in_1 = keys1 - keys2
    only_in_2 = keys2 - keys1
    common_keys = keys1 & keys2

    different = {}
    for key in common_keys:
        if dict1[key] != dict2[key]:
            different[key] = (dict1[key], dict2[key])

    return only_in_1, only_in_2, different


__all__ = ['dict_difference']
