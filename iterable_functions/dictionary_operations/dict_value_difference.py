"""
Calculate differences between two dictionaries.

This module provides a function to find differences between two dictionaries,
returning only the changed values without categorization.
"""

from typing import Any


def dict_value_difference(
    dict1: dict[str, Any], 
    dict2: dict[str, Any], 
    ignore_missing: bool = False
) -> dict[str, Any]:
    """
    Calculate the difference between two dictionaries.

    Parameters
    ----------
    dict1 : dict[str, Any]
        The first dictionary (base/original).
    dict2 : dict[str, Any]
        The second dictionary (modified/new).
    ignore_missing : bool, optional
        If True, ignore keys that are missing in dict2 (by default False).

    Returns
    -------
    dict[str, Any]
        A dictionary containing only the keys that have different values
        between dict1 and dict2, with values from dict2.

    Raises
    ------
    TypeError
        If parameters are of wrong type.

    Examples
    --------
    >>> dict1 = {'a': 1, 'b': 2, 'c': 3}
    >>> dict2 = {'a': 1, 'b': 5, 'd': 4}
    >>> dict_value_difference(dict1, dict2)
    {'b': 5, 'd': 4}
    >>> dict_value_difference(dict1, dict2, ignore_missing=True)
    {'b': 5}

    Notes
    -----
    This function performs a shallow comparison of dictionary values.
    For nested dictionaries, use dict_structural_difference for more detailed analysis.

    Complexity
    ----------
    Time: O(n), Space: O(k) where n is the total keys and k is different keys
    """
    # Input validation
    if not isinstance(dict1, dict):
        raise TypeError(f"dict1 must be a dictionary, got {type(dict1).__name__}")
    if not isinstance(dict2, dict):
        raise TypeError(f"dict2 must be a dictionary, got {type(dict2).__name__}")
    if not isinstance(ignore_missing, bool):
        raise TypeError(f"ignore_missing must be a boolean, got {type(ignore_missing).__name__}")

    differences = {}
    
    # Check all keys in dict2
    for key, value in dict2.items():
        if key not in dict1:
            # New key in dict2
            if not ignore_missing:
                differences[key] = value
        elif dict1[key] != value:
            # Key exists in both but values are different
            differences[key] = value
    
    # Check for keys that exist in dict1 but not in dict2
    if not ignore_missing:
        for key in dict1:
            if key not in dict2:
                # Key was removed in dict2, mark with None
                differences[key] = None
    
    return differences


__all__ = ["dict_value_difference"]
