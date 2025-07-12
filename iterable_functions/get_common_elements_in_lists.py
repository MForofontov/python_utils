from typing import Any

def get_common_elements_in_lists(list_of_lists: list[list[Any]]) -> list[Any]:
    """
    Finds common elements between various lists.

    Parameters
    ----------
    list_of_lists : list
        Contains a list of lists.

    Returns
    -------
    list
        Returns a list that contains the intersection of all elements inside the list of lists.

    Raises
    ------
    TypeError
        If list_of_lists is not a list of lists.
    """
    if not isinstance(list_of_lists, list) or not all(isinstance(lst, list) for lst in list_of_lists):
        raise TypeError("list_of_lists must be a list of lists")

    intersection_set = None
    for lst in list_of_lists:
        if intersection_set is None:
            intersection_set = set(lst)
        else:
            intersection_set.intersection_update(lst)

    return list(intersection_set) if intersection_set is not None else []
