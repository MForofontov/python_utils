"""
Simple XOR decryption.

This module provides XOR decryption functions that work with data encrypted
using the encrypt_xor function.
"""


def decrypt_xor(
    encrypted_data: str,
    key: str,
) -> str:
    """
    Decrypt data that was encrypted using XOR cipher.

    Parameters
    ----------
    encrypted_data : str
        The hex-encoded encrypted data to decrypt.
    key : str
        The key used for decryption (same as encryption key).

    Returns
    -------
    str
        The decrypted data as a string.

    Raises
    ------
    TypeError
        If encrypted_data or key is not a string.
    ValueError
        If encrypted_data or key is empty, or if encrypted_data is not valid hex.

    Examples
    --------
    >>> from .encrypt_xor import encrypt_xor
    >>> original = "Hello, World!"
    >>> encrypted, key = encrypt_xor(original)
    >>> decrypted = decrypt_xor(encrypted, key)
    >>> decrypted == original
    True

    Notes
    -----
    XOR decryption is identical to XOR encryption due to the properties
    of the XOR operation (A XOR B XOR B = A). This function reverses
    the encryption process to recover the original data.

    Complexity
    ----------
    Time: O(n) where n is the size of the encrypted data, Space: O(n)
    """
    # Input validation
    if not isinstance(encrypted_data, str):
        raise TypeError(
            f"encrypted_data must be a string, got {type(encrypted_data).__name__}"
        )
    if not isinstance(key, str):
        raise TypeError(f"key must be a string, got {type(key).__name__}")

    # Value validation
    if len(encrypted_data) == 0:
        raise ValueError("encrypted_data cannot be empty")
    if len(key) == 0:
        raise ValueError("key cannot be empty")

    # Validate hex format
    if len(encrypted_data) % 2 != 0:
        raise ValueError("encrypted_data must have even length (valid hex)")

    try:
        # Convert hex string to bytes
        encrypted_bytes = bytes.fromhex(encrypted_data)
    except ValueError as e:
        raise ValueError(f"encrypted_data must be valid hex string: {e}") from e

    # Convert key to bytes
    key_bytes = key.encode("utf-8")
    key_len = len(key_bytes)

    # Perform XOR decryption (same as encryption)
    decrypted_bytes = bytearray()

    for i, byte in enumerate(encrypted_bytes):
        decrypted_byte = byte ^ key_bytes[i % key_len]
        decrypted_bytes.append(decrypted_byte)

    try:
        # Convert back to string
        return decrypted_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"decryption resulted in invalid UTF-8: {e}") from e


__all__ = ["decrypt_xor"]
