def capitalize_words(s: str) -> str:
    """
    Capitalize the first letter of each word in a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with the first letter of each word capitalized.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> capitalize_words("hello world")
    'Hello World'
    >>> capitalize_words("python programming")
    'Python Programming'
    >>> capitalize_words("123 hello")
    '123 Hello'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s.title()


__all__ = ['capitalize_words']
