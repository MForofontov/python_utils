def repeat_string(s: str, n: int) -> str:
    """
    Repeat a string a specified number of times.

    Parameters
    ----------
    s : str
        The input string.
    n : int
        The number of times to repeat the string.

    Returns
    -------
    str
        The repeated string.

    Raises
    ------
    TypeError
        If the input string is not a string or the number of times is not an integer.

    Examples
    --------
    >>> repeat_string("hello", 3)
    'hellohellohello'
    >>> repeat_string("abc", 2)
    'abcabc'
    >>> repeat_string("test", 0)
    ''
    >>> repeat_string("repeat", -1)
    ''
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(n, int):
        raise TypeError("The number of times must be an integer.")
    return s * n

