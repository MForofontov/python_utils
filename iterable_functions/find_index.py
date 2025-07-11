
def find_index(input_list: list[str], target_string: str) -> int | None:
    """
    Find the index of a string in a list.

    Parameters
    ----------
    input_list : list
        The list to search.
    target_string : str
        The string to find.

    Returns
    -------
    int or None
        The index of the string in the list, or None if the string is not found.

    Raises
    ------
    TypeError
        If input_list is not a list or target_string is not a string.
    """
    if not isinstance(input_list, list):
        raise TypeError("input_list must be a list")
    if not all(isinstance(item, str) for item in input_list):
        raise TypeError("all elements in input_list must be strings")
    if not isinstance(target_string, str):
        raise TypeError("target_string must be a string")

    try:
        return input_list.index(target_string)
    except ValueError:
        return None
