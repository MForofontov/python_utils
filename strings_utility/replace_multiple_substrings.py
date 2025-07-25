def replace_multiple_substrings(s: str, replacements: dict[str, str]) -> str:
    """
    Replace multiple substrings in a string with specified replacements.

    Parameters
    ----------
    s : str
        The input string.
    replacements : Dict[str, str]
        A dictionary where keys are substrings to be replaced and values are the replacements.

    Returns
    -------
    str
        The string with specified substrings replaced.

    Raises
    ------
    TypeError
        If the input string is not a string or the replacements are not a dictionary.

    Examples
    --------
    >>> replace_multiple_substrings("hello world", {"hello": "hi", "world": "earth"})
    'hi earth'
    >>> replace_multiple_substrings("abc def ghi", {"abc": "123", "def": "456"})
    '123 456 ghi'
    >>> replace_multiple_substrings("foo bar baz", {"foo": "FOO", "bar": "BAR"})
    'FOO BAR baz'
    >>> replace_multiple_substrings("123 456 789", {"123": "one", "456": "two"})
    'one two 789'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(replacements, dict):
        raise TypeError("The replacements must be a dictionary.")

    for old, new in replacements.items():
        if not isinstance(old, str) or not isinstance(new, str):
            raise TypeError("Both keys and values in replacements must be strings.")
        s = s.replace(old, new)

    return s
