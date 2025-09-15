"""
Find differences between two dictionaries.

Parameters
----------
dict1 : dict
    The first dictionary.
dict2 : dict
    The second dictionary.
recursive : bool, optional
    If True, recursively compare nested dictionaries (default True).

Returns
-------
dict
    A dictionary containing the differences with keys:
    - 'added': keys present in dict2 but not in dict1
    - 'removed': keys present in dict1 but not in dict2
    - 'modified': keys present in both but with different values
    - 'unchanged': keys present in both with same values

Raises
------
TypeError
    If either dict1 or dict2 is not a dictionary.

Examples
--------
>>> d1 = {'a': 1, 'b': 2, 'c': {'d': 3}}
>>> d2 = {'a': 1, 'b': 3, 'e': 4, 'c': {'d': 4}}
>>> diff = dict_diff(d1, d2)
>>> diff['modified']
['b', 'c']
>>> diff['added']
['e']
"""

from typing import Any


def dict_diff(
    dict1: dict[str, Any], dict2: dict[str, Any], recursive: bool = True
) -> dict[str, list[str]]:
    """
    Find differences between two dictionaries.

    Parameters
    ----------
    dict1 : dict
        The first dictionary.
    dict2 : dict
        The second dictionary.
    recursive : bool, optional
        If True, recursively compare nested dictionaries (default True).

    Returns
    -------
    dict
        A dictionary containing the differences with keys:
        - 'added': keys present in dict2 but not in dict1
        - 'removed': keys present in dict1 but not in dict2
        - 'modified': keys present in both but with different values
        - 'unchanged': keys present in both with same values

    Raises
    ------
    TypeError
        If either dict1 or dict2 is not a dictionary.

    Examples
    --------
    >>> d1 = {'a': 1, 'b': 2, 'c': {'d': 3}}
    >>> d2 = {'a': 1, 'b': 3, 'e': 4, 'c': {'d': 4}}
    >>> diff = dict_diff(d1, d2)
    >>> diff['modified']
    ['b', 'c']
    >>> diff['added']
    ['e']
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        raise TypeError("Both dict1 and dict2 must be dictionaries")

    added = []
    removed = []
    modified = []
    unchanged = []

    # Check keys in dict1
    for key in dict1:
        if key not in dict2:
            removed.append(key)
        else:
            if (
                recursive
                and isinstance(dict1[key], dict)
                and isinstance(dict2[key], dict)
            ):
                if dict1[key] != dict2[key]:
                    modified.append(key)
                else:
                    unchanged.append(key)
            elif dict1[key] != dict2[key]:
                modified.append(key)
            else:
                unchanged.append(key)

    # Check keys in dict2
    for key in dict2:
        if key not in dict1:
            added.append(key)

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
    }


__all__ = ["dict_diff"]
