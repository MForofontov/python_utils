def join_strings(strings: list[str], delimiter: str = " ") -> str:
    """
    Join a list of strings into a single string with a specified delimiter.

    Parameters
    ----------
    strings : List[str]
        The list of strings to join.
    delimiter : str, optional
        The delimiter to join the strings with (default is space).

    Returns
    -------
    str
        The joined string.

    Raises
    ------
    TypeError
        If the input is not a list of strings or the delimiter is not a string.

    Examples
    --------
    >>> join_strings(['hello', 'world'])
    'hello world'
    >>> join_strings(['a', 'b', 'c'], delimiter=",")
    'a,b,c'
    >>> join_strings(['one', 'two', 'three'], delimiter=" - ")
    'one - two - three'
    >>> join_strings(['apple', 'banana', 'cherry'])
    'apple banana cherry'
    """
    if not isinstance(strings, list) or not all(
        isinstance(item, str) for item in strings
    ):
        raise TypeError("All elements in the list must be strings.")
    if not isinstance(delimiter, str):
        raise TypeError("The delimiter must be a string.")
    return delimiter.join(strings)

__all__ = ['join_strings']
