"""Pad numeric string with zeros on the left."""


def zfill_string(s: str, width: int) -> str:
    """
    Pad a numeric string on the left with zeros to fill a field of the specified width.

    Parameters
    ----------
    s : str
        The input string.
    width : int
        The width of the field.

    Returns
    -------
    str
        The string left-padded with zeros to the specified width.

    Raises
    ------
    TypeError
        If the input string is not a string or the width is not an integer.
    ValueError
        If the width is negative.

    Examples
    --------
    >>> zfill_string("42", 5)
    '00042'
    >>> zfill_string("-42", 5)
    '-0042'
    >>> zfill_string("123", 2)
    '123'
    >>> zfill_string("7", 3)
    '007'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(width, int):
        raise TypeError("The width must be an integer.")
    if width < 0:
        raise ValueError("The width must be non-negative.")

    return s.zfill(width)


__all__ = ["zfill_string"]
