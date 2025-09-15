from typing import Any


def remove_empty_dicts_recursive(nested_dict: dict[Any, Any]) -> dict[Any, Any]:
    """
    Recursively removes empty dictionary entries from a nested dictionary.

    Parameters
    ----------
    nested_dict : dict
        The nested dictionary.

    Returns
    -------
    dict
        The nested dictionary with empty dictionaries removed.

    Raises
    ------
    TypeError
        If nested_dict is not a dictionary.
    """
    if not isinstance(nested_dict, dict):
        raise TypeError("nested_dict must be a dictionary")

    def _remove_empty(d: dict[Any, Any]) -> dict[Any, Any]:
        if isinstance(d, dict):
            for key in list(d.keys()):
                d[key] = _remove_empty(d[key])
                if isinstance(d[key], dict) and not d[key]:
                    del d[key]
        return d

    return _remove_empty(nested_dict)


__all__ = ["remove_empty_dicts_recursive"]
