"""
Simple XOR encryption and decryption.

This module provides basic XOR encryption/decryption functions for educational
purposes and simple obfuscation. Note: XOR encryption is not cryptographically
secure and should not be used for protecting sensitive data.
"""

import secrets
from typing import Any


def encrypt_xor(
    data: str,
    key: str | None = None,
) -> tuple[str, str]:
    """
    Encrypt data using XOR cipher with a repeating key.

    Parameters
    ----------
    data : str
        The data to encrypt.
    key : str | None, optional
        The encryption key. If None, a random key is generated (by default None).

    Returns
    -------
    tuple[str, str]
        A tuple containing the encrypted data as hex string and the key.

    Raises
    ------
    TypeError
        If data or key is not a string.
    ValueError
        If data or key is empty.

    Examples
    --------
    >>> encrypted, key = encrypt_xor("Hello, World!")
    >>> len(encrypted) > 0
    True
    >>> len(key) > 0
    True
    >>> isinstance(encrypted, str)
    True
    >>> isinstance(key, str)
    True

    Notes
    -----
    XOR encryption is a simple cipher that XORs each byte of the data with
    the corresponding byte of the key (repeating the key as necessary).
    This is NOT cryptographically secure and should only be used for
    educational purposes or simple obfuscation.

    Complexity
    ----------
    Time: O(n) where n is the size of the data, Space: O(n)
    """
    # Input validation
    if not isinstance(data, str):
        raise TypeError(f"data must be a string, got {type(data).__name__}")
    if key is not None and not isinstance(key, str):
        raise TypeError(f"key must be a string or None, got {type(key).__name__}")
    
    # Value validation
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    if key is not None and len(key) == 0:
        raise ValueError("key cannot be empty")
    
    # Generate random key if not provided
    if key is None:
        key_length = max(8, len(data) // 4)  # Key length based on data size
        key = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 
                     for _ in range(key_length))
    
    # Convert data and key to bytes
    data_bytes = data.encode('utf-8')
    key_bytes = key.encode('utf-8')
    
    # Perform XOR encryption
    encrypted_bytes = bytearray()
    key_len = len(key_bytes)
    
    for i, byte in enumerate(data_bytes):
        encrypted_byte = byte ^ key_bytes[i % key_len]
        encrypted_bytes.append(encrypted_byte)
    
    # Convert to hex string
    encrypted_hex = encrypted_bytes.hex()
    
    return encrypted_hex, key


__all__ = ['encrypt_xor']
