"""
Generate random email for testing.
"""

import string

from .generate_random_string import generate_random_string


def generate_random_email(
    domain: str = "example.com",
    username_length: int = 10,
) -> str:
    """
    Generate a random email address.

    Parameters
    ----------
    domain : str, optional
        Email domain (by default "example.com").
    username_length : int, optional
        Length of username part (by default 10).

    Returns
    -------
    str
        Random email address.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If domain is empty or username_length is non-positive.

    Examples
    --------
    >>> email = generate_random_email()
    >>> '@example.com' in email
    True
    >>> email = generate_random_email("test.org", 5)
    >>> '@test.org' in email
    True

    Complexity
    ----------
    Time: O(n), Space: O(n)
    """
    if not isinstance(domain, str):
        raise TypeError(f"domain must be a string, got {type(domain).__name__}")
    if not isinstance(username_length, int):
        raise TypeError(
            f"username_length must be an integer, got {type(username_length).__name__}"
        )

    if len(domain) == 0:
        raise ValueError("domain cannot be empty")
    if username_length <= 0:
        raise ValueError(f"username_length must be positive, got {username_length}")

    username = generate_random_string(
        username_length, string.ascii_lowercase + string.digits
    )
    return f"{username}@{domain}"


__all__ = ["generate_random_email"]
