"""
Safely set a value in a nested dictionary, creating intermediate dictionaries as needed.

Parameters
----------
d : dict
    The dictionary to modify.
keys : str or list
    The key path where to set the value. Can be a dot-separated string or list of keys.
value : Any
    The value to set.

Returns
-------
None
    Modifies the dictionary in place.

Raises
------
TypeError
    If d is not a dictionary.

Examples
--------
>>> d = {'user': {'name': 'John'}}
>>> deep_set(d, 'user.profile.age', 30)
>>> d
{'user': {'name': 'John', 'profile': {'age': 30}}}
"""

from typing import Any, Dict, Union, List


def deep_set(d: Dict[str, Any], keys: Union[str, List[str]], value: Any) -> None:
    """
    Safely set a value in a nested dictionary, creating intermediate dictionaries as needed.

    Parameters
    ----------
    d : dict
        The dictionary to modify.
    keys : str or list
        The key path where to set the value. Can be a dot-separated string or list of keys.
    value : Any
        The value to set.

    Returns
    -------
    None
        Modifies the dictionary in place.

    Raises
    ------
    TypeError
        If d is not a dictionary.

    Examples
    --------
    >>> d = {'user': {'name': 'John'}}
    >>> deep_set(d, 'user.profile.age', 30)
    >>> d
    {'user': {'name': 'John', 'profile': {'age': 30}}}
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dictionary")

    if isinstance(keys, str):
        keys = keys.split('.')

    current = d
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value


__all__ = ['deep_set']
