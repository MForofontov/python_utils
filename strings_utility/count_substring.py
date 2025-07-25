def count_substring(s: str, substring: str) -> int:
    """
    Count the number of non-overlapping occurrences of a substring in a string.

    Parameters
    ----------
    s : str
        The input string.
    substring : str
        The substring to count.

    Returns
    -------
    int
        The number of non-overlapping occurrences of the substring.

    Raises
    ------
    TypeError
        If the input string or the substring is not a string.

    Examples
    --------
    >>> count_substring("hello world", "o")
    2
    >>> count_substring("ababab", "ab")
    3
    >>> count_substring("aaaa", "aa")
    2
    >>> count_substring("mississippi", "iss")
    2
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    if not isinstance(substring, str):
        raise TypeError("The substring must be a string.")
    return s.count(substring)
