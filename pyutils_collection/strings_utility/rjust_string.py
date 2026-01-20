"""Right-justify string in field of specified width."""


def rjust_string(s: str, width: int, fillchar: str = " ") -> str:
    """
    Right-justify a string in a field of a specified width.

    Parameters
    ----------
    s : str
        The input string.
    width : int
        The width of the field.
    fillchar : str, optional
        The character to fill the field with (default is space).

    Returns
    -------
    str
        The right-justified string.

    Raises
    ------
    TypeError
        If the input string is not a string, the width is not an integer, or the fill character is not a single character string.

    Examples
    --------
    >>> rjust_string("hello", 10)
    '     hello'
    >>> rjust_string("hello", 10, '-')
    '-----hello'
    >>> rjust_string("test", 8, '*')
    '****test'
    >>> rjust_string("example", 7)
    'example'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(width, int):
        raise TypeError("The width must be an integer.")
    if not isinstance(fillchar, str) or len(fillchar) != 1:
        raise TypeError("The fill character must be a single character string.")
    return s.rjust(width, fillchar)


__all__ = ["rjust_string"]
