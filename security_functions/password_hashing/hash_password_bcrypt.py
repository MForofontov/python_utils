"""
Password hashing using bcrypt algorithm.

This module provides secure password hashing using the bcrypt algorithm,
which is considered one of the most secure password hashing methods available.
"""

import bcrypt
from typing import Any


def hash_password_bcrypt(
    password: str,
    rounds: int = 12,
) -> str:
    """
    Hash a password using bcrypt with a configurable number of rounds.

    Parameters
    ----------
    password : str
        The plaintext password to hash.
    rounds : int, optional
        The number of rounds for bcrypt hashing (by default 12).
        Higher values are more secure but slower.

    Returns
    -------
    str
        The bcrypt hashed password as a string.

    Raises
    ------
    TypeError
        If password is not a string or rounds is not an integer.
    ValueError
        If password is empty or rounds is not in valid range (4-31).

    Examples
    --------
    >>> hashed = hash_password_bcrypt("my_secret_password")
    >>> len(hashed) == 60  # bcrypt hashes are always 60 characters
    True
    >>> hashed.startswith("$2b$")  # bcrypt identifier
    True
    >>> hash_password_bcrypt("password", rounds=10)  # doctest: +SKIP
    '$2b$10$...'

    Notes
    -----
    The bcrypt algorithm automatically handles salt generation and incorporates
    it into the hash. The resulting hash contains the salt, cost factor, and
    hash value in a single string.

    Complexity
    ----------
    Time: O(2^rounds), Space: O(1)
    """
    # Input validation
    if not isinstance(password, str):
        raise TypeError(f"password must be a string, got {type(password).__name__}")
    if not isinstance(rounds, int):
        raise TypeError(f"rounds must be an integer, got {type(rounds).__name__}")
    
    # Value validation
    if len(password) == 0:
        raise ValueError("password cannot be empty")
    if not (4 <= rounds <= 31):
        raise ValueError(f"rounds must be between 4 and 31, got {rounds}")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')


__all__ = ['hash_password_bcrypt']
