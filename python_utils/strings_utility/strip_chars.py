"""Strip specified characters from both ends."""


def strip_chars(s: str, chars: str) -> str:
    """
    Strip specified characters from both ends of a string.

    Parameters
    ----------
    s : str
        The input string.
    chars : str
        The characters to strip.

    Returns
    -------
    str
        The string with specified characters stripped from both ends.

    Raises
    ------
    TypeError
        If the input string or the characters to strip are not strings.

    Examples
    --------
    >>> strip_chars("...hello...", ".")
    'hello'
    >>> strip_chars("xyzhellozyx", "xyz")
    'hello'
    >>> strip_chars("123abc123", "123")
    'abc'
    >>> strip_chars("!!!hello!!!", "!")
    'hello'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(chars, str):
        raise TypeError("The characters to strip must be a string.")
    return s.strip(chars)


__all__ = ["strip_chars"]
