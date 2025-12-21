"""Remove all numerical digits from string."""


def remove_digits(s: str) -> str:
    """
    Remove all numerical digits from a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with all numerical digits removed.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> remove_digits("abc123")
    'abc'
    >>> remove_digits("12345")
    ''
    >>> remove_digits("hello123world")
    'helloworld'
    >>> remove_digits("no digits here")
    'no digits here'
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    return "".join(char for char in s if not char.isdigit())


__all__ = ["remove_digits"]
