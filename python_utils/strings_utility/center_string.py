"""Center string in field of specified width."""


def center_string(s: str, width: int, fillchar: str = " ") -> str:
    """
    Center a string in a field of a specified width.

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
        The centered string.

    Raises
    ------
    TypeError
        If the input string is not a string, the width is not an integer, or the fill character is not a single character string.

    Examples
    --------
    >>> center_string("hello", 11)
    '   hello   '
    >>> center_string("hello", 11, '-')
    '---hello---'
    >>> center_string("hello", 5)
    'hello'
    >>> center_string("hello", 10, '*')
    '**hello***'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    if not isinstance(width, int):
        raise TypeError("The width must be an integer.")
    if not isinstance(fillchar, str) or len(fillchar) != 1:
        raise TypeError("The fill character must be a single character string.")
    return s.center(width, fillchar)


__all__ = ["center_string"]
