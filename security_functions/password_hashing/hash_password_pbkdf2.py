"""
Password hashing using PBKDF2 algorithm.

This module provides secure password hashing using PBKDF2 with SHA-256,
which is widely supported and recommended by security standards.
"""

import hashlib
import secrets


def hash_password_pbkdf2(
    password: str,
    salt: bytes | None = None,
    iterations: int = 100000,
) -> tuple[str, bytes]:
    """
    Hash a password using PBKDF2 with SHA-256.

    Parameters
    ----------
    password : str
        The plaintext password to hash.
    salt : bytes | None, optional
        The salt to use for hashing. If None, a random salt is generated
        (by default None).
    iterations : int, optional
        The number of iterations for PBKDF2 (by default 100000).

    Returns
    -------
    tuple[str, bytes]
        A tuple containing the hashed password as hex string and the salt bytes.

    Raises
    ------
    TypeError
        If password is not a string, salt is not bytes or None,
        or iterations is not an integer.
    ValueError
        If password is empty or iterations is less than 1000.

    Examples
    --------
    >>> hashed, salt = hash_password_pbkdf2("my_secret_password")
    >>> len(hashed) == 64  # SHA-256 hex string length
    True
    >>> len(salt) == 32  # Default salt length
    True
    >>> isinstance(hashed, str)
    True
    >>> isinstance(salt, bytes)
    True

    Notes
    -----
    PBKDF2 (Password-Based Key Derivation Function 2) is defined in RFC 2898
    and is widely supported across different platforms and languages.
    The function returns both the hash and salt for storage.

    Complexity
    ----------
    Time: O(iterations), Space: O(1)
    """
    # Input validation
    if not isinstance(password, str):
        raise TypeError(f"password must be a string, got {type(password).__name__}")
    if salt is not None and not isinstance(salt, bytes):
        raise TypeError(f"salt must be bytes or None, got {type(salt).__name__}")
    if not isinstance(iterations, int):
        raise TypeError(
            f"iterations must be an integer, got {type(iterations).__name__}"
        )

    # Value validation
    if len(password) == 0:
        raise ValueError("password cannot be empty")
    if iterations < 1000:
        raise ValueError(
            f"iterations must be at least 1000 for security, got {iterations}"
        )

    # Generate salt if not provided
    if salt is None:
        salt = secrets.token_bytes(32)

    # Hash password using PBKDF2
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

    return hashed.hex(), salt


__all__ = ["hash_password_pbkdf2"]
