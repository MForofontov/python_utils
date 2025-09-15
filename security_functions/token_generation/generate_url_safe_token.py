"""
URL-safe token generation.

This module provides functions for generating URL-safe tokens that can be
safely used in URLs, file names, and other contexts where special characters
might cause issues.
"""

import secrets
import base64


def generate_url_safe_token(
    length: int = 32,
) -> str:
    """
    Generate a URL-safe random token.

    Parameters
    ----------
    length : int, optional
        The desired length of the token in characters (by default 32).
        Note: The actual length may be slightly different due to base64 encoding.

    Returns
    -------
    str
        A URL-safe random token containing only alphanumeric characters,
        hyphens, and underscores.

    Raises
    ------
    TypeError
        If length is not an integer.
    ValueError
        If length is less than 1.

    Examples
    --------
    >>> token = generate_url_safe_token(16)
    >>> len(token) >= 16  # May be slightly longer due to base64 encoding
    True
    >>> all(c.isalnum() or c in '-_' for c in token)
    True
    >>> token = generate_url_safe_token(32)
    >>> isinstance(token, str)
    True

    Notes
    -----
    This function generates random bytes and encodes them using URL-safe
    base64 encoding, which uses only alphanumeric characters, hyphens,
    and underscores. The token is safe for use in URLs without encoding.

    Complexity
    ----------
    Time: O(length), Space: O(length)
    """
    # Input validation
    if not isinstance(length, int):
        raise TypeError(f"length must be an integer, got {type(length).__name__}")

    # Value validation
    if length < 1:
        raise ValueError(f"length must be at least 1, got {length}")

    # Calculate number of bytes needed for approximately the desired length
    # Base64 encoding produces 4 characters for every 3 bytes
    num_bytes = ((length * 3) + 3) // 4

    # Generate random bytes and encode as URL-safe base64
    random_bytes = secrets.token_bytes(num_bytes)
    token = base64.urlsafe_b64encode(random_bytes).decode("ascii")

    # Remove padding and truncate to desired length
    token = token.rstrip("=")
    return token[:length] if len(token) > length else token


__all__ = ["generate_url_safe_token"]
