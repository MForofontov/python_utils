import re


def identify_string_in_dict_lists_regex(
    target_value: str,
    dict_of_lists: dict[str | int, list[list[str]]],
    regex: str = None,
) -> str | int | bool:
    """
    Identifies if a string is present in any list inside a dictionary.

    Parameters
    ----------
    target_value : str
        The value to find.
    dict_of_lists : dict
        A dictionary where the values are lists of lists.
    regex : str, optional
        A regex pattern to search for in the lists.

    Returns
    -------
    int or str or bool
        The key of the entry where the string is present, or False if not found.

    Raises
    ------
    TypeError
        If target_value is not a string, dict_of_lists is not a dictionary, or regex is not a string or None.
    """
    if not isinstance(target_value, str):
        raise TypeError("target_value must be a string")
    if not isinstance(dict_of_lists, dict):
        raise TypeError("dict_of_lists must be a dictionary")
    if not all(
        isinstance(value, list) and all(isinstance(sublist, list) for sublist in value)
        for value in dict_of_lists.values()
    ):
        raise TypeError("All values in dict_of_lists must be lists of lists")
    if regex is not None and not isinstance(regex, str):
        raise TypeError("regex must be a string or None")

    for key, lists in dict_of_lists.items():
        for list_ in lists:
            if regex:
                if any(re.search(regex, item) for item in list_):
                    return key
            else:
                if target_value in list_:
                    return key
    return False
