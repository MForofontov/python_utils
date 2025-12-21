"""Strip leading and trailing whitespace."""


def strip_whitespace(s: str) -> str:
    """
    Strip leading and trailing whitespace from a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with leading and trailing whitespace removed.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> strip_whitespace("  hello world  ")
    'hello world'
    >>> strip_whitespace("\t\nhello\n\t")
    'hello'
    >>> strip_whitespace("   no leading or trailing spaces   ")
    'no leading or trailing spaces'
    >>> strip_whitespace("no_whitespace")
    'no_whitespace'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s.strip()


__all__ = ["strip_whitespace"]
