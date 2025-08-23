import string


def remove_punctuation(s: str) -> str:
    """
    Remove all punctuation characters from a string.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The string with all punctuation characters removed.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> remove_punctuation("hello, world!")
    'hello world'
    >>> remove_punctuation("a.b,c!")
    'abc'
    >>> remove_punctuation("123!@#")
    '123'
    >>> remove_punctuation("no punctuation")
    'no punctuation'
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    return s.translate(str.maketrans("", "", string.punctuation))


__all__ = ['remove_punctuation']
