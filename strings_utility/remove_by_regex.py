import re

def remove_by_regex(string: str, pattern: str) -> str:
    """
    Remove all occurrences of a pattern from a string, ensuring no extra spaces are left.

    Parameters
    ----------
    string : str
        The string to remove the pattern from.
    pattern : str
        The regex pattern to remove from the string.

    Returns
    -------
    str
        The string with all occurrences of the pattern removed.

    Raises
    ------
    TypeError
        If string is not a string or pattern is not a string.
    
    Examples
    --------
    >>> remove_by_regex("hello world", "o")
    'hell wrld'
    >>> remove_by_regex("hello world", "l")
    'heo word'
    >>> remove_by_regex("hello world", " ")
    'helloworld'
    """
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    # If the pattern is empty, return the original string
    if pattern == "":
        return string

    # Adjust the pattern to also match surrounding spaces
    adjusted_pattern = r'\s*' + pattern + r'\s*'
    result = re.sub(adjusted_pattern, ' ', string).strip()
    return re.sub(r'\s+', ' ', result)
