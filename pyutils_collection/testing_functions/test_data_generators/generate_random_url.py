"""
Generate random URL for testing.
"""

import random
import string

from .generate_random_string import generate_random_string


def generate_random_url(
    protocol: str = "https",
    domain: str = "example.com",
    path_length: int = 3,
) -> str:
    """
    Generate a random URL.

    Parameters
    ----------
    protocol : str, optional
        URL protocol (by default "https").
    domain : str, optional
        URL domain (by default "example.com").
    path_length : int, optional
        Number of path segments (by default 3).

    Returns
    -------
    str
        Random URL.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If protocol or domain is empty, or path_length is negative.

    Examples
    --------
    >>> url = generate_random_url()
    >>> url.startswith('https://example.com/')
    True
    >>> url = generate_random_url("http", "test.org", 2)
    >>> url.startswith('http://test.org/')
    True

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(protocol, str):
        raise TypeError(f"protocol must be a string, got {type(protocol).__name__}")
    if not isinstance(domain, str):
        raise TypeError(f"domain must be a string, got {type(domain).__name__}")
    if not isinstance(path_length, int):
        raise TypeError(
            f"path_length must be an integer, got {type(path_length).__name__}"
        )

    if len(protocol) == 0:
        raise ValueError("protocol cannot be empty")
    if len(domain) == 0:
        raise ValueError("domain cannot be empty")
    if path_length < 0:
        raise ValueError(f"path_length must be non-negative, got {path_length}")

    path_segments = [
        generate_random_string(random.randint(5, 10), string.ascii_lowercase)
        for _ in range(path_length)
    ]
    path = "/".join(path_segments)

    if path:
        return f"{protocol}://{domain}/{path}"
    return f"{protocol}://{domain}"


__all__ = ["generate_random_url"]
