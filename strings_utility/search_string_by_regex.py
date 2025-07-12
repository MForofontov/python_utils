import re

def search_string_by_regex(pattern: str, string: str) -> str | None:
    r"""
    Searches for a regex pattern in a string.

    Parameters
    ----------
    pattern : str
        The regex pattern to search for.
    string : str
        The string to search in.

    Returns
    -------
    str or None
        The match object if the pattern is found, original string otherwise.

    Raises
    ------
    TypeError
        If pattern or string is not a string.
    
    Examples
    --------
    >>> search_string_by_regex(r"\d+", "abc123xyz")
    '123'
    >>> search_string_by_regex(r"\d+", "hello world")
    None
    >>> search_string_by_regex(r'[a-z]+', "123")
    None
    """
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    if pattern == "":
        return None

    match = re.search(pattern, string)
    return match.group(0) if match else None
