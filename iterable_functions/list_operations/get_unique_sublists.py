from typing import TypeVar

T = TypeVar("T")


def get_unique_sublists(list_of_lists: list[list[T]]) -> list[list[T]]:
    """
    Identify unique sublists within a list of lists.

    Parameters
    ----------
    list_of_lists : list[list[T]]
        The list containing various sublists.

    Returns
    -------
    list[list[T]]
        List containing unique sublists.

    Raises
    ------
    TypeError
        If list_of_lists is not a list of lists.
    ValueError
        If any sublist contains unhashable elements.
    """
    if not isinstance(list_of_lists, list):
        raise TypeError("list_of_lists must be a list")
    if not all(isinstance(sublist, list) for sublist in list_of_lists):
        raise TypeError("All elements of list_of_lists must be lists")

    seen = set()
    unique_sublists = []
    for sublist in list_of_lists:
        sublist_tuple = tuple(sublist)
        try:
            if sublist_tuple not in seen:
                seen.add(sublist_tuple)
                unique_sublists.append(sublist)
        except TypeError as e:
            raise ValueError(f"Sublist contains unhashable elements: {e}") from e
    return unique_sublists


__all__ = ["get_unique_sublists"]
