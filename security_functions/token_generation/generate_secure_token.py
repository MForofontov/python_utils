"""
Secure random token generation.

This module provides functions for generating cryptographically secure
random tokens for various purposes like session tokens, API keys, etc.
"""

import secrets
import string


def generate_secure_token(
    length: int = 32,
    include_letters: bool = True,
    include_digits: bool = True,
    include_symbols: bool = False,
) -> str:
    """
    Generate a cryptographically secure random token.

    Parameters
    ----------
    length : int, optional
        The length of the token to generate (by default 32).
    include_letters : bool, optional
        Whether to include letters in the token (by default True).
    include_digits : bool, optional
        Whether to include digits in the token (by default True).
    include_symbols : bool, optional
        Whether to include symbols in the token (by default False).

    Returns
    -------
    str
        A cryptographically secure random token.

    Raises
    ------
    TypeError
        If parameters are not of the correct type.
    ValueError
        If length is less than 1 or no character types are selected.

    Examples
    --------
    >>> token = generate_secure_token(16)
    >>> len(token) == 16
    True
    >>> token.isalnum()  # Only letters and digits by default
    True
    >>> token_with_symbols = generate_secure_token(8, include_symbols=True)
    >>> len(token_with_symbols) == 8
    True

    Notes
    -----
    This function uses the secrets module which is designed for generating
    cryptographically strong random numbers suitable for managing secrets.
    The character set is customizable based on the boolean parameters.

    Complexity
    ----------
    Time: O(length), Space: O(length)
    """
    # Input validation
    if not isinstance(length, int):
        raise TypeError(f"length must be an integer, got {type(length).__name__}")
    if not isinstance(include_letters, bool):
        raise TypeError(f"include_letters must be a boolean, got {type(include_letters).__name__}")
    if not isinstance(include_digits, bool):
        raise TypeError(f"include_digits must be a boolean, got {type(include_digits).__name__}")
    if not isinstance(include_symbols, bool):
        raise TypeError(f"include_symbols must be a boolean, got {type(include_symbols).__name__}")
    
    # Value validation
    if length < 1:
        raise ValueError(f"length must be at least 1, got {length}")
    if not (include_letters or include_digits or include_symbols):
        raise ValueError("at least one character type must be included")
    
    # Build character set
    charset = ""
    if include_letters:
        charset += string.ascii_letters
    if include_digits:
        charset += string.digits
    if include_symbols:
        charset += "!@#$%^&*-_=+[]{}|;:,.<>?"
    
    # Generate token
    return ''.join(secrets.choice(charset) for _ in range(length))


__all__ = ['generate_secure_token']
