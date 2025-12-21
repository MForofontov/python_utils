"""Check if string ends with specified suffix."""


def ends_with(s: str, suffix: str) -> bool:
    """
    Check if a string ends with a specified suffix.

    Parameters
    ----------
    s : str
        The input string.
    suffix : str
        The suffix to check.

    Returns
    -------
    bool
        True if the string ends with the suffix, False otherwise.

    Raises
    ------
    TypeError
        If the input string or the suffix is not a string.

    Examples
    --------
    >>> ends_with("hello world", "world")
    True
    >>> ends_with("hello world", "hello")
    False
    >>> ends_with("abc123", "123")
    True
    >>> ends_with("abc123", "456")
    False
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    if not isinstance(suffix, str):
        raise TypeError("The suffix must be a string.")
    return s.endswith(suffix)


__all__ = ["ends_with"]
