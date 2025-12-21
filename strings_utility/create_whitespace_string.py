"""Create whitespace-filled string of same length."""


def create_whitespace_string(input_string: str) -> str:
    """
    Create a string with the same length as the input string filled with whitespace.

    Parameters
    ----------
    input_string : str
        Input string to get the size from.

    Returns
    -------
    str
        String containing the same number of white spaces as the length of the input string.

    Raises
    ------
    TypeError
        If input_string is not a string.

    Examples
    --------
    >>> create_whitespace_string("hello")
    '     '
    >>> create_whitespace_string("hello world")
    '           '
    >>> create_whitespace_string(" ")
    ' '
    """
    if not isinstance(input_string, str):
        raise TypeError("input_string must be a string")

    return " " * len(input_string)


__all__ = ["create_whitespace_string"]
