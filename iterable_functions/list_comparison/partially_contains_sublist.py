from typing import TypeVar

from .any_match_lists import any_match_lists

T = TypeVar("T")


def partially_contains_sublist(
    main_list: list[T], list_of_lists: list[list[T]]
) -> bool:
    """
    Check if elements of the main list are partially contained in any sublist of the list of lists.

    Parameters
    ----------
    main_list : list[T]
        The query list to check for partial containment.
    list_of_lists : list[list[T]]
        The subject list containing sublists to compare against the query list.

    Returns
    -------
    bool
        True if any element of the main list is partially contained in any sublist of the list of lists, False otherwise.

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
        if any_match_lists(main_list, sublist):
            return True
    return False


__all__ = ["partially_contains_sublist"]
