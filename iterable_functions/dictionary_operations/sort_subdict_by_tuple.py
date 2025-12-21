from collections import OrderedDict
"""Dictionary sorting by tuple keys."""

from typing import Any


def sort_subdict_by_tuple(
    dict_: dict[str, dict[str, Any]], order: tuple[str, ...]
) -> dict[str, OrderedDict[str, Any]]:
    """
    Sorts the sub-dictionaries of a given dictionary based on a specified order tuple.

    Parameters
    ----------
    dict_ : dict[str, dict[str, Any]]
        The input dictionary containing sub-dictionaries as values.
    order : tuple[str, ...]
        A tuple specifying the desired order of keys in the sorted sub-dictionaries.

    Returns
    -------
    dict[str, OrderedDict[str, Any]]
        A new dictionary with each sub-dictionary sorted according to the specified order.

    Raises
    ------
    TypeError
        If dict_ is not a dictionary of dictionaries or order is not a tuple of strings.
    """
    if not isinstance(dict_, dict) or not all(
        isinstance(subdict, dict) for subdict in dict_.values()
    ):
        raise TypeError("dict_ must be a dictionary with sub-dictionaries as values")
    if not isinstance(order, tuple) or not all(isinstance(item, str) for item in order):
        raise TypeError("order must be a tuple of strings")

    sorted_data: dict[str, OrderedDict[str, Any]] = {}
    for key, subdict in dict_.items():
        sorted_subdict = OrderedDict(
            sorted(
                subdict.items(),
                key=lambda item: (
                    order.index(item[0]) if item[0] in order else len(order)
                ),
            )
        )
        sorted_data[key] = sorted_subdict
    return sorted_data


__all__ = ["sort_subdict_by_tuple"]
