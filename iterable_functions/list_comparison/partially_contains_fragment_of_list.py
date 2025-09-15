from typing import Any


def partially_contains_fragment_of_list(
    target_list: list[Any], list_of_lists: list[list[Any]]
) -> bool:
    """
    Check if the target_list is contained inside sublist even if it partially.
    e.g partially_contains_fragment_of_list(['a', 'b'], [['a', 'b', 'c'], ['d', 'e']])
    returns True.

    Parameters
    ----------
    target_list : list
        List to find inside the list_of_lists.
    list_of_lists : list
        The nested list.

    Returns
    -------
    bool
        True if contains False if not.

    Raises
    ------
    TypeError
        If target_list is not a list or list_of_lists is not a list of lists.
    """
    if not isinstance(target_list, list):
        raise TypeError("target_list must be a list")
    if not isinstance(list_of_lists, list) or not all(
        isinstance(sublist, list) for sublist in list_of_lists
    ):
        raise TypeError("list_of_lists must be a list of lists")

    for sub in list_of_lists:
        if any(
            sub[i : i + len(target_list)] == target_list
            for i in range(len(sub) - len(target_list) + 1)
        ):
            return True
    return False


__all__ = ["partially_contains_fragment_of_list"]
