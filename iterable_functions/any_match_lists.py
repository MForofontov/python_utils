from typing import Any


def any_match_lists(list1: list[Any], list2: list[Any]) -> bool:
    """
    Check if any element of list1 is contained in list2.

    Parameters
    ----------
    list1 : list
        The query list to check for partial containment.
    list2 : list
        The subject list to compare against the query list.

    Returns
    -------
    bool
        True if any element of list1 is found in list2, False otherwise.

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
        return any(elem in list2 for elem in list1)
    except TypeError as e:
        raise TypeError(f"An element in the list cannot be compared: {e}")

__all__ = ['any_match_lists']
