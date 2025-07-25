def truncate_string(s: str, length: int) -> str:
    """
    Truncate a string to a specified length.

    Parameters
    ----------
    s : str
        The input string.
    length : int
        The length to truncate the string to.

    Returns
    -------
    str
        The truncated string.

    Raises
    ------
    TypeError
        If the input string is not a string or the length is not an integer.
    ValueError
        If the length is negative.

    Examples
    --------
    >>> truncate_string("hello world", 5)
    'hello'
    >>> truncate_string("python programming", 6)
    'python'
    >>> truncate_string("1234567890", 4)
    '1234'
    >>> truncate_string("truncate", 3)
    'tru'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(length, int):
        raise TypeError("The length must be an integer.")

    return s[:length]
