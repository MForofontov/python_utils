def rstrip_chars(s: str, chars: str) -> str:
    """
    Strip specified characters from the right end of a string.

    Parameters
    ----------
    s : str
        The input string.
    chars : str
        The characters to strip.

    Returns
    -------
    str
        The string with specified characters stripped from the right end.

    Raises
    ------
    TypeError
        If the input string or the characters to strip are not strings.

    Examples
    --------
    >>> rstrip_chars("...hello...", ".")
    '...hello'
    >>> rstrip_chars("xyzhellozyx", "xyz")
    'xyzhello'
    >>> rstrip_chars("123abc123", "123")
    '123abc'
    >>> rstrip_chars("!!!hello!!!", "!")
    '!!!hello'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(chars, str):
        raise TypeError("The characters to strip must be a string.")
    return s.rstrip(chars)

__all__ = ['rstrip_chars']
