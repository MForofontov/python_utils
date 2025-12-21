"""AES encryption and decryption utilities."""

import base64

from cryptography.fernet import Fernet


def encrypt_data_aes(
    data: str | bytes,
    key: str | bytes | None = None,
) -> tuple[str, str]:
    """
    Encrypt data using AES encryption via Fernet.

    Parameters
    ----------
    data : str | bytes
        The data to encrypt.
    key : str | bytes | None, optional
        The encryption key. If None, a new key is generated (by default None).

    Returns
    -------
    tuple[str, str]
        A tuple containing the encrypted data as base64 string and the key
        as base64 string.

    Raises
    ------
    TypeError
        If data or key is not of the correct type.
    ValueError
        If data is empty or key is invalid.

    Examples
    --------
    >>> encrypted, key = encrypt_data_aes("Hello, World!")
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
    This function uses Fernet symmetric encryption, which is part of the
    cryptography library and provides authenticated encryption. The key
    is URL-safe base64 encoded and suitable for storage.

    Complexity
    ----------
    Time: O(n) where n is the size of the data, Space: O(n)
    """
    # Input validation
    if not isinstance(data, (str, bytes)):
        raise TypeError(f"data must be str or bytes, got {type(data).__name__}")
    if key is not None and not isinstance(key, (str, bytes)):
        raise TypeError(f"key must be str, bytes, or None, got {type(key).__name__}")

    # Value validation
    if isinstance(data, str) and len(data) == 0:
        raise ValueError("data cannot be empty")
    if isinstance(data, bytes) and len(data) == 0:
        raise ValueError("data cannot be empty")

    # Generate key if not provided
    if key is None:
        fernet_key = Fernet.generate_key()
    else:
        if isinstance(key, str):
            try:
                fernet_key = base64.urlsafe_b64decode(key.encode("utf-8"))
                if len(fernet_key) != 32:
                    raise ValueError("key must be 32 bytes when decoded")
                fernet_key = key.encode("utf-8")
            except Exception as e:
                raise ValueError(f"invalid key format: {e}") from e
        else:
            if len(key) == 32:
                fernet_key = base64.urlsafe_b64encode(key)
            elif len(key) == 44:  # base64 encoded 32 bytes
                fernet_key = key
            else:
                raise ValueError(
                    "key must be either 32 bytes or 44 character base64 string"
                )

    # Create Fernet instance
    try:
        fernet = Fernet(fernet_key)
    except Exception as e:
        raise ValueError(f"invalid encryption key: {e}") from e

    # Convert data to bytes if necessary
    if isinstance(data, str):
        data_bytes = data.encode("utf-8")
    else:
        data_bytes = data

    # Encrypt data
    try:
        encrypted_data = fernet.encrypt(data_bytes)
        return base64.b64encode(encrypted_data).decode("utf-8"), fernet_key.decode(
            "utf-8"
        )
    except Exception as e:
        raise ValueError(f"encryption failed: {e}") from e


__all__ = ["encrypt_data_aes"]
