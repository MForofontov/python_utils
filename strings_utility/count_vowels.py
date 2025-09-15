def count_vowels(s: str) -> int:
    """
    Count the number of vowels in a string (English).

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    int
        The number of vowels in the input string.

    Raises
    ------
    TypeError
        If the input is not a string.

    Examples
    --------
    >>> count_vowels("hello")
    2
    >>> count_vowels("world")
    1
    >>> count_vowels("aeiou")
    5
    >>> count_vowels("bcdfghjklmnpqrstvwxyz")
    0
    """
    if not isinstance(s, str):
        raise TypeError("The input must be a string.")
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)


__all__ = ["count_vowels"]
