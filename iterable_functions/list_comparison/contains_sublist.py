from typing import Any
from .all_match_lists import all_match_lists


def contains_sublist(main_list: list[Any], list_of_lists: list[list[Any]]) -> bool:
    """
    Check if elements of the main list are fully contained in any sublist of the list of lists.

    Parameters
    ----------
    main_list : list
        The query list to check for full containment.
    list_of_lists : list
        The subject list containing sublists to compare against the query list.

    Returns
    -------
    bool
        True if all elements of the main list are fully contained in any sublist of the list of lists, False otherwise.

    Raises
    ------
    TypeError
        If main_list is not a list or list_of_lists is not a list of lists.
    """
    if not isinstance(main_list, list):
        raise TypeError("main_list must be a list")
    if not isinstance(list_of_lists, list) or not all(
        isinstance(sublist, list) for sublist in list_of_lists
    ):
        raise TypeError("list_of_lists must be a list of lists")

    for sublist in list_of_lists:
        if all_match_lists(main_list, sublist):
            return True
    return False


__all__ = ["contains_sublist"]
