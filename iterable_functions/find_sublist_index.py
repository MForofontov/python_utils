from typing import Any

def find_sublist_index(input_list_of_lists: list[list[Any]], target_value: Any) -> int | None:
    """
    Finds the index of the sublist that contains the target value within a list of lists.

    Parameters
    ----------
    input_list_of_lists : list of list
        The list of lists to search.
    target_value : any
        The value to find.

    Returns
    -------
    int or None
        The index of the sublist containing the element, or None if the string is not found in any sublist.

    Raises
    ------
    TypeError
        If input_list_of_lists is not a list of lists.
    """
    if not isinstance(input_list_of_lists, list) or not all(isinstance(sublist, list) for sublist in input_list_of_lists):
        raise TypeError("input_list_of_lists must be a list of lists")

    for index, sublist in enumerate(input_list_of_lists):
        if target_value in sublist:
            return index
    return None
