"""
Filter dictionary by keys using patterns or exact matches.

Parameters
----------
d : dict
    The dictionary to filter.
keys : list or set
    Keys to include in the filtered dictionary.
pattern : str, optional
    Regex pattern to match keys against.
invert : bool, optional
    If True, exclude matching keys instead of including them (default False).

Returns
-------
dict
    A filtered dictionary.

Raises
------
TypeError
    If d is not a dictionary or keys is not a list/set.

Examples
--------
>>> d = {'name': 'John', 'age': 30, 'city': 'NYC', 'email': 'john@example.com'}
>>> filter_dict_by_keys(d, ['name', 'age'])
{'name': 'John', 'age': 30}
"""

import re
from typing import Any


def filter_dict_by_keys(
    d: dict[str, Any],
    keys: list[str] | set[str] = None,
    pattern: str = None,
    invert: bool = False,
) -> dict[str, Any]:
    """
    Filter dictionary by keys using patterns or exact matches.

    Parameters
    ----------
    d : dict
        The dictionary to filter.
    keys : list or set, optional
        Keys to include in the filtered dictionary.
    pattern : str, optional
        Regex pattern to match keys against.
    invert : bool, optional
        If True, exclude matching keys instead of including them (default False).

    Returns
    -------
    dict
        A filtered dictionary.

    Raises
    ------
    TypeError
        If d is not a dictionary or keys is not a list/set.

    Examples
    --------
    >>> d = {'name': 'John', 'age': 30, 'city': 'NYC', 'email': 'john@example.com'}
    >>> filter_dict_by_keys(d, ['name', 'age'])
    {'name': 'John', 'age': 30}
    """
    if not isinstance(d, dict):
        raise TypeError(f"d must be a dictionary, got {type(d).__name__}")

    if keys is not None and not isinstance(keys, (list, set)):
        raise TypeError(f"keys must be a list or set, got {type(keys).__name__}")

    filtered = {}

    for key, value in d.items():
        include = False

        if keys is not None:
            include = key in keys
        elif pattern is not None:
            include = bool(re.search(pattern, key))
        else:
            include = True

        if invert:
            include = not include

        if include:
            filtered[key] = value

    return filtered


__all__ = ["filter_dict_by_keys"]
