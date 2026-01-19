"""
Generate random string for testing.
"""

import random
import string


def generate_random_string(
    length: int = 10,
    charset: str = string.ascii_letters + string.digits,
) -> str:
    """
    Generate a random string of specified length.

    Parameters
    ----------
    length : int, optional
        Length of the string to generate (by default 10).
    charset : str, optional
        Character set to use for generation (by default ascii letters + digits).

    Returns
    -------
    str
        Randomly generated string.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If length is non-positive or charset is empty.

    Examples
    --------
    >>> result = generate_random_string(5)
    >>> len(result)
    5
    >>> result = generate_random_string(10, string.ascii_lowercase)
    >>> len(result)
    10

    Notes
    -----
    Uses Python's random module for generation.

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(length, int):
        raise TypeError(f"length must be an integer, got {type(length).__name__}")
    if not isinstance(charset, str):
        raise TypeError(f"charset must be a string, got {type(charset).__name__}")

    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")
    if len(charset) == 0:
        raise ValueError("charset cannot be empty")

    return "".join(random.choice(charset) for _ in range(length))


__all__ = ["generate_random_string"]
