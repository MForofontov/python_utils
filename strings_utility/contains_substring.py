def contains_substring(s: str, substring: str) -> bool:
    """
    Check if a string contains a specified substring.

    Parameters
    ----------
    s : str
        The input string.
    substring : str
        The substring to check for.

    Returns
    -------
    bool
        True if the string contains the substring, False otherwise.

    Raises
    ------
    TypeError
        If the input string or the substring is not a string.

    Examples
    --------
    >>> contains_substring("hello world", "world")
    True
    >>> contains_substring("hello world", "there")
    False
    >>> contains_substring("abc123", "123")
    True
    >>> contains_substring("abc123", "456")
    False
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    if not isinstance(substring, str):
        raise TypeError("The substring must be a string.")
    return substring in s

__all__ = ['contains_substring']
