from typing import Any


def all_match_lists(list1: list[Any], list2: list[Any]) -> bool:
    """
    Check if all elements of list1 are contained in list2.

    Parameters
    ----------
    list1 : list
        The query list to check for full containment.
    list2 : list
        The subject list to compare against the query list.

    Returns
    -------
    bool
        True if all elements of list1 are found in list2, False otherwise.

    Raises
    ------
    TypeError
        If list1 or list2 is not a list or contains unhashable elements.
    """
    if not isinstance(list1, list):
        raise TypeError("list1 must be a list")
    if not isinstance(list2, list):
        raise TypeError("list2 must be a list")

    try:
        return all(elem in list2 for elem in list1)
    except TypeError as exc:
        raise TypeError(
            f"An element in the list cannot be compared: {exc}"
        ) from exc


__all__ = ["all_match_lists"]
