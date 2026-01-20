import pytest

try:
    from cryptography.fernet import Fernet
    from python_utils.security_functions.encryption_helpers.decrypt_data_aes import decrypt_data_aes
    from python_utils.security_functions.encryption_helpers.encrypt_data_aes import encrypt_data_aes
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None  # type: ignore
    decrypt_data_aes = None  # type: ignore
    encrypt_data_aes = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.security,
    pytest.mark.skipif(not CRYPTOGRAPHY_AVAILABLE, reason="cryptography not installed"),
]


def test_decrypt_data_aes_basic_decryption() -> None:
    """
    Test case 1: Basic AES decryption should recover original data.
    """
    # Arrange
    original_data = "Hello, World!"
    encrypted, key = encrypt_data_aes(original_data)

    # Act
    decrypted = decrypt_data_aes(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_data_aes_custom_key_decryption() -> None:
    """
    Test case 2: Decrypt data encrypted with custom key.
    """
    # Arrange
    original_data = "Test message with custom key"
    from cryptography.fernet import Fernet

    custom_key = Fernet.generate_key().decode("utf-8")
    encrypted, _ = encrypt_data_aes(original_data, key=custom_key)

    # Act
    decrypted = decrypt_data_aes(encrypted, custom_key)

    # Assert
    assert decrypted == original_data


def test_decrypt_data_aes_unicode_data() -> None:
    """
    Test case 3: Handle Unicode characters in data.
    """
    # Arrange
    original_data = "Hello 世界! 🌍 ümläuts"
    encrypted, key = encrypt_data_aes(original_data)

    # Act
    decrypted = decrypt_data_aes(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_data_aes_long_data() -> None:
    """
    Test case 4: Decrypt long data string.
    """
    # Arrange
    original_data = "This is a very long message that spans multiple lines. " * 100
    encrypted, key = encrypt_data_aes(original_data)

    # Act
    decrypted = decrypt_data_aes(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_data_aes_special_characters() -> None:
    """
    Test case 5: Handle special characters and symbols.
    """
    # Arrange
    original_data = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
    encrypted, key = encrypt_data_aes(original_data)

    # Act
    decrypted = decrypt_data_aes(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_data_aes_bytes_to_string_conversion() -> None:
    """
    Test case 6: Decrypt bytes data that was encrypted.
    """
    # Arrange
    original_bytes = b"Byte data test"
    encrypted, key = encrypt_data_aes(original_bytes)

    # Act
    decrypted = decrypt_data_aes(encrypted, key)

    # Assert
    # Should return the string representation of the original bytes
    assert decrypted == original_bytes.decode("utf-8")


def test_decrypt_data_aes_roundtrip_multiple_times() -> None:
    """
    Test case 7: Multiple encrypt/decrypt roundtrips should be consistent.
    """
    # Arrange
    original_data = "Roundtrip test data"
    from cryptography.fernet import Fernet

    key = Fernet.generate_key().decode("utf-8")

    # Act - Multiple roundtrips
    encrypted1, _ = encrypt_data_aes(original_data, key=key)
    decrypted1 = decrypt_data_aes(encrypted1, key)

    encrypted2, _ = encrypt_data_aes(decrypted1, key=key)
    decrypted2 = decrypt_data_aes(encrypted2, key)

    # Assert
    assert decrypted1 == original_data
    assert decrypted2 == original_data


def test_decrypt_data_aes_type_validation() -> None:
    """
    Test case 8: Type validation for parameters.
    """
    # Test invalid encrypted_data type
    with pytest.raises(TypeError, match="encrypted_data must be a string"):
        decrypt_data_aes(123, "key")

    # Test invalid key type
    with pytest.raises(TypeError, match="key must be a string"):
        decrypt_data_aes("encrypted", 123)


def test_decrypt_data_aes_value_validation() -> None:
    """
    Test case 9: Value validation for parameters.
    """
    # Test empty encrypted_data
    with pytest.raises(ValueError, match="encrypted_data cannot be empty"):
        decrypt_data_aes("", "key")

    # Test empty key
    with pytest.raises(ValueError, match="key cannot be empty"):
        decrypt_data_aes("encrypted", "")


def test_decrypt_data_aes_wrong_key() -> None:
    """
    Test case 10: Wrong key should raise ValueError during decryption.
    """
    # Arrange
    original_data = "Secret message"
    encrypted, correct_key = encrypt_data_aes(original_data)
    from cryptography.fernet import Fernet

    wrong_key = Fernet.generate_key().decode("utf-8")

    # Act & Assert
    with pytest.raises(ValueError, match="decryption failed"):
        decrypt_data_aes(encrypted, wrong_key)


def test_decrypt_data_aes_invalid_encrypted_data() -> None:
    """
    Test case 11: Invalid encrypted data should raise ValueError.
    """
    # Arrange
    _, key = encrypt_data_aes("test")
    invalid_encrypted = "not_valid_encrypted_data"

    # Act & Assert
    with pytest.raises(ValueError, match="decryption failed"):
        decrypt_data_aes(invalid_encrypted, key)


def test_decrypt_data_aes_invalid_key_format() -> None:
    """
    Test case 12: Invalid key format should raise ValueError.
    """
    # Arrange
    encrypted, _ = encrypt_data_aes("test")
    invalid_key = "not_a_valid_fernet_key"

    # Act & Assert
    with pytest.raises(ValueError, match="decryption failed"):
        decrypt_data_aes(encrypted, invalid_key)
