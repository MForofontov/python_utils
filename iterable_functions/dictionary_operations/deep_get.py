"""
Safely get a value from a nested dictionary using dot notation or list of keys.

Parameters
----------
d : dict
    The dictionary to search.
keys : str or list
    The key path to search for. Can be a dot-separated string or list of keys.
default : Any, optional
    Default value to return if key path is not found (default None).

Returns
-------
Any
    The value at the specified key path, or default if not found.

Raises
------
TypeError
    If d is not a dictionary.

Examples
--------
>>> d = {'user': {'name': 'John', 'profile': {'age': 30}}}
>>> deep_get(d, 'user.name')
'John'
>>> deep_get(d, ['user', 'profile', 'age'])
30
>>> deep_get(d, 'user.email', 'not found')
'not found'
"""

from typing import Any


def deep_get(d: dict[str, Any], keys: str | list[str], default: Any = None) -> Any:
    """
    Safely get a value from a nested dictionary using dot notation or list of keys.

    Parameters
    ----------
    d : dict
        The dictionary to search.
    keys : str or list
        The key path to search for. Can be a dot-separated string or list of keys.
    default : Any, optional
        Default value to return if key path is not found (default None).

    Returns
    -------
    Any
        The value at the specified key path, or default if not found.

    Raises
    ------
    TypeError
        If d is not a dictionary.

    Examples
    --------
    >>> d = {'user': {'name': 'John', 'profile': {'age': 30}}}
    >>> deep_get(d, 'user.name')
    'John'
    >>> deep_get(d, ['user', 'profile', 'age'])
    30
    >>> deep_get(d, 'user.email', 'not found')
    'not found'
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dictionary")

    if isinstance(keys, str):
        keys = keys.split(".")

    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


__all__ = ["deep_get"]
