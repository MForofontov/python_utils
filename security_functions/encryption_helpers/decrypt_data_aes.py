"""
AES decryption utilities.

This module provides functions for AES decryption using Fernet symmetric
encryption from the cryptography library.
"""

from cryptography.fernet import Fernet
import base64


def decrypt_data_aes(
    encrypted_data: str,
    key: str,
) -> str:
    """
    Decrypt data that was encrypted using AES encryption via Fernet.

    Parameters
    ----------
    encrypted_data : str
        The base64 encoded encrypted data to decrypt.
    key : str
        The base64 encoded encryption key used for decryption.

    Returns
    -------
    str
        The decrypted data as a string.

    Raises
    ------
    TypeError
        If encrypted_data or key is not a string.
    ValueError
        If encrypted_data or key is empty, invalid, or decryption fails.

    Examples
    --------
    >>> from .encrypt_data_aes import encrypt_data_aes
    >>> original = "Hello, World!"
    >>> encrypted, key = encrypt_data_aes(original)
    >>> decrypted = decrypt_data_aes(encrypted, key)
    >>> decrypted == original
    True

    Notes
    -----
    This function uses Fernet symmetric decryption to recover the original
    data. The encrypted_data and key must be the same as returned from
    the encrypt_data_aes function.

    Complexity
    ----------
    Time: O(n) where n is the size of the encrypted data, Space: O(n)
    """
    # Input validation
    if not isinstance(encrypted_data, str):
        raise TypeError(f"encrypted_data must be a string, got {type(encrypted_data).__name__}")
    if not isinstance(key, str):
        raise TypeError(f"key must be a string, got {type(key).__name__}")
    
    # Value validation
    if len(encrypted_data) == 0:
        raise ValueError("encrypted_data cannot be empty")
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    try:
        # Decode the base64 encoded key
        fernet_key = key.encode('utf-8')
        fernet = Fernet(fernet_key)
        
        # Decode the base64 encoded encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        
        # Decrypt the data
        decrypted_bytes = fernet.decrypt(encrypted_bytes)
        
        # Convert back to string
        return decrypted_bytes.decode('utf-8')
        
    except Exception as e:
        raise ValueError(f"decryption failed: {e}") from e


__all__ = ['decrypt_data_aes']
