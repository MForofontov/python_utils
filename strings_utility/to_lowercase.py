def to_lowercase(s: str) -> str:
    """
    Convert all characters in a string to lowercase.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with all characters converted to lowercase.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> to_lowercase("Hello World")
    'hello world'
    >>> to_lowercase("PYTHON")
    'python'
    >>> to_lowercase("12345")
    '12345'
    >>> to_lowercase("!@#")
    '!@#'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s.lower()

__all__ = ['to_lowercase']
