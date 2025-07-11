import re

def regex_present(regex_list: list[str], string: str) -> bool:
    """
    Check if any regex in a list is found in a string.

    Parameters
    ----------
    regex_list : list of str
        The list of regexes to search for in the string.
    string : str
        The string to search in.

    Returns
    -------
    bool
        True if any regex is found in the string, False otherwise.

    Raises
    ------
    TypeError
        If regex_list is not a list of strings or string is not a string.
    
    Examples
    --------
    >>> regex_present(["[0-9]", "[a-z]"], "123")
    True
    >>> regex_present(["[0-9]", "[a-z]"], "abc")
    True
    >>> regex_present(["[0-9]", "[a-z]"], "ABC")
    False
    """
    if not isinstance(regex_list, list):
        raise TypeError("regex_list must be a list")
    if not all(isinstance(regex, str) for regex in regex_list):
        raise TypeError("all elements in regex_list must be strings")
    if not isinstance(string, str):
        raise TypeError("string must be a string")

    return any(re.search(regex, string) for regex in regex_list)