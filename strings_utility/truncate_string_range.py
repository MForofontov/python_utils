"""Truncate string to specified range."""


def truncate_string_range(s: str, start: int, end: int) -> str:
    """
    Truncate a string to a specified range.

    Parameters
    ----------
    s : str
        The input string.
    start : int
        The starting index of the range. Negative values are allowed.
    end : int
        The ending index of the range. Negative values are allowed.

    Returns
    -------
    str
        The truncated string.

    Raises
    ------
    TypeError
        If the input string is not a string or if the start or end indices are not integers.
    ValueError
        If the start index is greater than the end index.

    Examples
    --------
    >>> truncate_string_range("hello world", 0, 5)
    'hello'
    >>> truncate_string_range("python programming", 7, 18)
    'programming'
    >>> truncate_string_range("1234567890", 2, 5)
    '345'
    >>> truncate_string_range("truncate", 0, 4)
    'trun'
    >>> truncate_string_range("hello world", -5, -1)
    'worl'
    """
    if not isinstance(s, str):
        raise TypeError("The input string must be a string.")
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("The start and end indices must be integers.")
    if start > end:
        raise ValueError("The start index must be less than or equal to the end index.")

    return s[start:end]


__all__ = ["truncate_string_range"]
