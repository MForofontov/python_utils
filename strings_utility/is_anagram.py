from collections import Counter


def is_anagram(string_1: str, string_2: str) -> bool:
    """
    Check if two strings are anagrams.

    Parameters
    ----------
    string_1 : str
        The first string.
    string_2 : str
        The second string.

    Returns
    -------
    bool
        True if the strings are anagrams, False otherwise.

    Raises
    ------
    TypeError
        If either of the inputs is not a string.

    Examples
    --------
    >>> is_anagram("listen", "silent")
    True
    >>> is_anagram("hello", "world")
    False
    >>> is_anagram("a!b@c#", "c@b!a#")
    True
    """
    if not isinstance(string_1, str) or not isinstance(string_2, str):
        raise TypeError("Both inputs must be strings")

    # Remove any whitespace and convert to lowercase
    string_1 = string_1.replace(" ", "").lower()
    string_2 = string_2.replace(" ", "").lower()

    # Use Counter to compare the frequency of characters in both strings
    return Counter(string_1) == Counter(string_2)


__all__ = ["is_anagram"]
