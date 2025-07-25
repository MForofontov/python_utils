def remove_whitespace(s: str) -> str:
    """
    Remove all whitespace characters from a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with all whitespace characters removed.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> remove_whitespace("hello world")
    'helloworld'
    >>> remove_whitespace(" a b c ")
    'abc'
    >>> remove_whitespace(" \t\nhello \t\nworld \t\n")
    'helloworld'
    >>> remove_whitespace("no_whitespace")
    'no_whitespace'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return "".join(s.split())
