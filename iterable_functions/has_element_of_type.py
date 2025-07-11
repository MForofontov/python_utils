from typing import Any

def has_element_of_type(input_list: list[Any], target_type: type) -> bool:
    """
    Check if any element in the input list matches the specified target type.

    Parameters
    ----------
    input_list : list
        The list to check for the presence of the target type.
    target_type : type
        The type to search for within the input list.

    Returns
    -------
    bool
        True if the target type is found in the input list, False otherwise.

    Raises
    ------
    TypeError
        If input_list is not a list or target_type is not a type.
    """
    if not isinstance(input_list, list):
        raise TypeError("input_list must be a list")
    if not isinstance(target_type, type):
        raise TypeError("target_type must be a type")

    for element in input_list:
        if isinstance(element, target_type):
            return True
    return False
