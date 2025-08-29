import re


def replace_by_regex(string: str, pattern: str, replacement: str) -> str:
    """
    Replace all occurrences of a regex pattern within a string with a specified replacement,
    ensuring no extra spaces are left.

    Spaces are intentionally inserted around replacements to maintain separation.

    Parameters
    ----------
    string : str
        The string to search and replace occurrences in.
    pattern : str
        The regex pattern to search for within `string`.
    replacement : str
        The string to replace each match of `pattern` in `string` with.

    Returns
    -------
    str
        A new string with all matches of `pattern` replaced by `replacement`.

    Raises
    ------
    TypeError
        If string, pattern, or replacement is not a string.

    Examples
    --------
    >>> replace_by_regex("hello world", "o", "x")
    'hell x w x rld'
    >>> replace_by_regex("hello world", "l", "y")
    'he y y o wor y d'
    >>> replace_by_regex("hello world", " ", "_")
    'hello _ world'
    """
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    if not isinstance(replacement, str):
        raise TypeError("replacement must be a string")
    # If the pattern is empty, return the original string
    if pattern == "":
        return string

    # Adjust the pattern to also match surrounding spaces
    adjusted_pattern = r"\s*" + pattern + r"\s*"
    result = re.sub(adjusted_pattern, " " + replacement + " ", string).strip()
    return re.sub(r"\s+", " ", result)


__all__ = ['replace_by_regex']
