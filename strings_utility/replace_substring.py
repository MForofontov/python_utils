def replace_substring(s: str, old: str, new: str) -> str:
    """
    Replace all occurrences of a substring with another substring in a string.

    Parameters
    ----------
    s : str
        The input string.
    old : str
        The substring to be replaced.
    new : str
        The substring to replace with.

    Returns
    -------
    str
        The string with the specified substring replaced.

    Raises
    ------
    TypeError
        If the input string, the old substring, or the new substring is not a string.

    Examples
    --------
    >>> replace_substring("hello world", "world", "earth")
    'hello earth'
    >>> replace_substring("abc def ghi", "def", "123")
    'abc 123 ghi'
    >>> replace_substring("foo bar baz", "bar", "BAR")
    'foo BAR baz'
    >>> replace_substring("123 456 789", "456", "two")
    '123 two 789'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(old, str):
        raise TypeError("The old substring must be a string.")
    if not isinstance(new, str):
        raise TypeError("The new substring must be a string.")
    # If old is an empty string, return the original because there is '' between each character
    if old == "":
        return s

    return s.replace(old, new)


__all__ = ["replace_substring"]
