def replace_tabs(s: str, tabsize: int = 4) -> str:
    """
    Replace all tab characters in a string with a specified number of spaces.

    Parameters
    ----------
    s : str
        The input string.
    tabsize : int, optional
        The number of spaces to replace each tab character with (default is 4).

    Returns
    -------
    str
        The string with all tab characters replaced by the specified number of spaces.

    Raises
    ------
    TypeError
        If the input string is not a string or the tab size is not an integer.
    ValueError
        If the tab size is negative.

    Examples
    --------
    >>> replace_tabs("hello\tworld")
    'hello    world'
    >>> replace_tabs("hello\tworld", 2)
    'hello  world'
    >>> replace_tabs("hello\tworld", 8)
    'hello        world'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(tabsize, int):
        raise TypeError("The tab size must be an integer.")
    if tabsize < 0:
        raise ValueError("The tab size must be non-negative.")

    return s.replace("\t", " " * tabsize)


__all__ = ['replace_tabs']
