import base64

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.security]
from security_functions.encryption_helpers.encrypt_data_aes import encrypt_data_aes


def test_encrypt_data_aes_string_data_auto_key() -> None:
    """
    Test case 1: Encrypt string data with auto-generated key.
    """
    # Arrange
    data = "Hello, World!"

    # Act
    encrypted, key = encrypt_data_aes(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0
    assert len(key) > 0
    assert encrypted != data  # Should be encrypted
    # Verify base64 format
    try:
        base64.b64decode(encrypted)
    except Exception:
        pytest.fail("Encrypted data should be valid base64")


def test_encrypt_data_aes_bytes_data_auto_key() -> None:
    """
    Test case 2: Encrypt bytes data with auto-generated key.
    """
    # Arrange
    data = b"Hello, World!"

    # Act
    encrypted, key = encrypt_data_aes(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0
    assert len(key) > 0


def test_encrypt_data_aes_string_data_custom_key() -> None:
    """
    Test case 3: Encrypt string data with custom key.
    """
    # Arrange
    data = "Test message"
    # Generate a valid Fernet key
    from cryptography.fernet import Fernet

    custom_key = Fernet.generate_key().decode("utf-8")

    # Act
    encrypted, returned_key = encrypt_data_aes(data, key=custom_key)

    # Assert
    assert isinstance(encrypted, str)
    assert returned_key == custom_key
    assert len(encrypted) > 0


def test_encrypt_data_aes_unicode_data() -> None:
    """
    Test case 4: Handle Unicode characters in data.
    """
    # Arrange
    data = "Hello 世界! 🌍 ümläuts"

    # Act
    encrypted, key = encrypt_data_aes(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0


def test_encrypt_data_aes_long_data() -> None:
    """
    Test case 5: Encrypt long data string.
    """
    # Arrange
    data = "This is a very long message that spans multiple lines. " * 100

    # Act
    encrypted, key = encrypt_data_aes(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0


def test_encrypt_data_aes_different_data_different_results() -> None:
    """
    Test case 6: Different data should produce different encrypted results.
    """
    # Arrange
    data1 = "Message 1"
    data2 = "Message 2"
    from cryptography.fernet import Fernet

    same_key = Fernet.generate_key().decode("utf-8")

    # Act
    encrypted1, _ = encrypt_data_aes(data1, key=same_key)
    encrypted2, _ = encrypt_data_aes(data2, key=same_key)

    # Assert
    assert encrypted1 != encrypted2


def test_encrypt_data_aes_same_data_different_keys() -> None:
    """
    Test case 7: Same data with different keys should produce different results.
    """
    # Arrange
    data = "Same data"
    from cryptography.fernet import Fernet

    key1 = Fernet.generate_key().decode("utf-8")
    key2 = Fernet.generate_key().decode("utf-8")

    # Act
    encrypted1, _ = encrypt_data_aes(data, key=key1)
    encrypted2, _ = encrypt_data_aes(data, key=key2)

    # Assert
    assert encrypted1 != encrypted2


def test_encrypt_data_aes_bytes_key_handling() -> None:
    """
    Test case 8: Handle bytes key input.
    """
    # Arrange
    data = "Test message"
    from cryptography.fernet import Fernet

    key_bytes = Fernet.generate_key()

    # Act
    encrypted, returned_key = encrypt_data_aes(data, key=key_bytes)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(returned_key, str)
    assert len(encrypted) > 0


def test_encrypt_data_aes_special_characters() -> None:
    """
    Test case 9: Handle special characters and symbols.
    """
    # Arrange
    data = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"

    # Act
    encrypted, key = encrypt_data_aes(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0


def test_encrypt_data_aes_type_validation() -> None:
    """
    Test case 10: Type validation for parameters.
    """
    # Test invalid data type
    with pytest.raises(TypeError, match="data must be str or bytes"):
        encrypt_data_aes(123)

    # Test invalid key type
    with pytest.raises(TypeError, match="key must be str, bytes, or None"):
        encrypt_data_aes("data", key=123)


def test_encrypt_data_aes_value_validation() -> None:
    """
    Test case 11: Value validation for parameters.
    """
    # Test empty string data
    with pytest.raises(ValueError, match="data cannot be empty"):
        encrypt_data_aes("")

    # Test empty bytes data
    with pytest.raises(ValueError, match="data cannot be empty"):
        encrypt_data_aes(b"")


def test_encrypt_data_aes_invalid_key_format() -> None:
    """
    Test case 12: Invalid key format should raise ValueError.
    """
    # Test invalid key format
    with pytest.raises(ValueError, match="invalid key format"):
        encrypt_data_aes("data", key="invalid_key")

    # Test key with wrong length
    with pytest.raises(ValueError, match="key must be 32 bytes when decoded"):
        encrypt_data_aes("data", key=base64.urlsafe_b64encode(b"short").decode("utf-8"))
