"""Remove all non-alphanumeric characters."""


def remove_non_alphanumeric(s: str) -> str:
    """
    Remove all non-alphanumeric characters from a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with all non-alphanumeric characters removed.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> remove_non_alphanumeric("abc123!@#")
    'abc123'
    >>> remove_non_alphanumeric("hello world!")
    'helloworld'
    >>> remove_non_alphanumeric("123-456-7890")
    '1234567890'
    >>> remove_non_alphanumeric("no_special_chars")
    'nospecialchars'
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string.")
    return "".join(char for char in s if char.isalnum())


__all__ = ["remove_non_alphanumeric"]
