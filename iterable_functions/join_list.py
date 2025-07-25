def join_list(lst: list[str], delimiter: str) -> str:
    """
    Join all elements in a list into a single string.

    Parameters
    ----------
    lst : list
        List with elements to be joined.
    delimiter : str
        Character used to join list elements.

    Returns
    -------
    str
        A single string with all elements in the input list joined by the character chosen as link.

    Raises
    ------
    TypeError
        If lst is not a list of strings or delimiter is not a string.
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not all(isinstance(item, str) for item in lst):
        raise TypeError("all elements in lst must be strings")
    if not isinstance(delimiter, str):
        raise TypeError("delimiter must be a string")

    return delimiter.join(lst)
