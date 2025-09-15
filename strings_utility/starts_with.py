def starts_with(s: str, prefix: str) -> bool:
    """
    Check if a string starts with a specified prefix.

    Parameters
    ----------
    s : str
        The input string.
    prefix : str
        The prefix to check.

    Returns
    -------
    bool
        True if the string starts with the prefix, False otherwise.

    Raises
    ------
    TypeError
        If the input string or the prefix is not a string.

    Examples
    --------
    >>> starts_with("hello world", "hello")
    True
    >>> starts_with("hello world", "world")
    False
    >>> starts_with("abc123", "abc")
    True
    >>> starts_with("abc123", "123")
    False
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(prefix, str):
        raise TypeError("The prefix must be a string.")
    return s.startswith(prefix)


__all__ = ["starts_with"]
