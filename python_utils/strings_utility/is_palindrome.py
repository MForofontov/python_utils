def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    bool
        True if the string is a palindrome, False otherwise.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> is_palindrome("racecar")
    True
    >>> is_palindrome("hello")
    False
    >>> is_palindrome("A man a plan a canal Panama")
    False
    >>> is_palindrome("Able was I ere I saw Elba")
    False
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s == s[::-1]


__all__ = ['is_palindrome']
