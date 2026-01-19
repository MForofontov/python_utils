"""Strip specified characters from left end."""


def lstrip_chars(s: str, chars: str) -> str:
    """
    Strip specified characters from the left end of a string.

    Parameters
    ----------
    s : str
        The input string.
    chars : str
        The characters to strip.

    Returns
    -------
    str
        The string with specified characters stripped from the left end.

    Raises
    ------
    TypeError
        If the input string or the characters to strip are not strings.

    Examples
    --------
    >>> lstrip_chars("...hello...", ".")
    'hello...'
    >>> lstrip_chars("xyzhellozyx", "xyz")
    'hellozyx'
    >>> lstrip_chars("123abc123", "123")
    'abc123'
    >>> lstrip_chars("!!!hello!!!", "!")
    'hello!!!'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(chars, str):
        raise TypeError("The characters to strip must be a string.")
    return s.lstrip(chars)


__all__ = ["lstrip_chars"]
