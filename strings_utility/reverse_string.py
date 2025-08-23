def reverse_string(s: str) -> str:
    """
    Reverse the characters in a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with characters in reverse order.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> reverse_string("hello")
    'olleh'
    >>> reverse_string("world")
    'dlrow'
    >>> reverse_string("12345")
    '54321'
    >>> reverse_string("!@#")
    '#@!'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s[::-1]


__all__ = ['reverse_string']
