def to_uppercase(s: str) -> str:
    """
    Convert all characters in a string to uppercase.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with all characters converted to uppercase.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> to_uppercase("hello world")
    'HELLO WORLD'
    >>> to_uppercase("python")
    'PYTHON'
    >>> to_uppercase("12345")
    '12345'
    >>> to_uppercase("!@#")
    '!@#'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s.upper()


__all__ = ['to_uppercase']
