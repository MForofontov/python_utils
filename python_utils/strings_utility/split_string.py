def split_string(s: str, delimiter: str = " ") -> list[str]:
    """
    Split a string by a specified delimiter.

    Parameters
    ----------
    s : str
        The input string.
    delimiter : str, optional
        The delimiter to split the string by (default is space).

    Returns
    -------
    List[str]
        A list of substrings.

    Raises
    ------
    TypeError
        If the input string or the delimiter is not a string.

    Examples
    --------
    >>> split_string("hello world")
    ['hello', 'world']
    >>> split_string("a,b,c", delimiter=",")
    ['a', 'b', 'c']
    >>> split_string("one,two,three", delimiter=",")
    ['one', 'two', 'three']
    >>> split_string("apple banana cherry")
    ['apple', 'banana', 'cherry']
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(delimiter, str):
        raise TypeError("The delimiter must be a string.")
    return s.split(delimiter)


__all__ = ['split_string']
