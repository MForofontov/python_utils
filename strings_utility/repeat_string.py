def repeat_string(s: str, n: int) -> str:
    """
    Repeat a string a specified number of times.

    Parameters
    ----------
    s : str
        The input string.
    n : int
        The number of times to repeat the string. Must be non-negative.

    Returns
    -------
    str
        The repeated string.

    Raises
    ------
    TypeError
        If the input string is not a string or the number of times is not an integer.
    ValueError
        If the number of times is negative.

    Examples
    --------
    >>> repeat_string("hello", 3)
    'hellohellohello'
    >>> repeat_string("abc", 2)
    'abcabc'
    >>> repeat_string("test", 0)
    ''
    >>> repeat_string("repeat", -1)
    Traceback (most recent call last):
        ...
    ValueError: The number of times must be non-negative.
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if type(n) is not int:
        raise TypeError("The number of times must be an integer.")
    if n < 0:
        raise ValueError("The number of times must be non-negative.")
    return s * n


__all__ = ["repeat_string"]
