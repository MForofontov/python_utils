def swapcase_string(s: str) -> str:
    """
    Swap the case of each character in a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with the case of each character swapped.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> swapcase_string("Hello World")
    'hELLO wORLD'
    >>> swapcase_string("Python3.8")
    'pYTHON3.8'
    >>> swapcase_string("12345")
    '12345'
    >>> swapcase_string("!@#")
    '!@#'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s.swapcase()

__all__ = ['swapcase_string']
