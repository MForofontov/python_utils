"""
Flatten a nested dictionary into a single-level dictionary.

Parameters
----------
d : dict
    The dictionary to flatten.
separator : str, optional
    The separator to use for nested keys (default '_').
prefix : str, optional
    A prefix to add to all keys (default '').

Returns
-------
dict
    A flattened dictionary.

Raises
------
TypeError
    If d is not a dictionary.

Examples
--------
>>> nested = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
>>> flatten_dict(nested)
{'a': 1, 'b_c': 2, 'b_d_e': 3}
"""

from typing import Any


def flatten_dict(
    d: dict[str, Any], separator: str = "_", prefix: str = ""
) -> dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dictionary.

    Parameters
    ----------
    d : dict
        The dictionary to flatten.
    separator : str, optional
        The separator to use for nested keys (default '_').
    prefix : str, optional
        A prefix to add to all keys (default '').

    Returns
    -------
    dict
        A flattened dictionary.

    Raises
    ------
    TypeError
        If d is not a dictionary.

    Examples
    --------
    >>> nested = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
    >>> flatten_dict(nested)
    {'a': 1, 'b_c': 2, 'b_d_e': 3}
    """
    if not isinstance(d, dict):
        raise TypeError(f"d must be a dictionary, got {type(d).__name__}")

    flattened = {}

    for key, value in d.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key

        if isinstance(value, dict):
            flattened.update(flatten_dict(value, separator, new_key))
        else:
            flattened[new_key] = value

    return flattened


__all__ = ["flatten_dict"]
