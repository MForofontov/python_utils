import pytest

pytestmark = [pytest.mark.unit, pytest.mark.security]
from python_utils.security_functions.encryption_helpers.encrypt_xor import encrypt_xor


def test_encrypt_xor_basic_encryption() -> None:
    """
    Test case 1: Basic XOR encryption with default parameters.
    """
    # Arrange
    data = "Hello, World!"

    # Act
    encrypted, key = encrypt_xor(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0
    assert len(key) > 0
    assert encrypted != data  # Should be encrypted
    # Verify hex format
    assert all(c in "0123456789abcdef" for c in encrypted)


def test_encrypt_xor_custom_key() -> None:
    """
    Test case 2: XOR encryption with custom key.
    """
    # Arrange
    data = "Test message"
    custom_key = "mykey123"

    # Act
    encrypted, returned_key = encrypt_xor(data, key=custom_key)

    # Assert
    assert isinstance(encrypted, str)
    assert returned_key == custom_key
    assert len(encrypted) > 0
    assert all(c in "0123456789abcdef" for c in encrypted)


def test_encrypt_xor_different_keys_different_results() -> None:
    """
    Test case 3: Different keys should produce different encrypted results.
    """
    # Arrange
    data = "Same data"
    key1 = "key1"
    key2 = "key2"

    # Act
    encrypted1, _ = encrypt_xor(data, key=key1)
    encrypted2, _ = encrypt_xor(data, key=key2)

    # Assert
    assert encrypted1 != encrypted2


def test_encrypt_xor_random_key_generation() -> None:
    """
    Test case 4: Random key generation produces different keys.
    """
    # Arrange
    data = "Test data"

    # Act
    _, key1 = encrypt_xor(data)
    _, key2 = encrypt_xor(data)

    # Assert
    assert key1 != key2
    assert len(key1) > 0
    assert len(key2) > 0


def test_encrypt_xor_unicode_data() -> None:
    """
    Test case 5: Handle Unicode characters in data.
    """
    # Arrange
    data = "Hello 世界! 🌍 ümläuts"

    # Act
    encrypted, key = encrypt_xor(data)

    # Assert
    assert isinstance(encrypted, str)
    assert isinstance(key, str)
    assert len(encrypted) > 0
    assert all(c in "0123456789abcdef" for c in encrypted)


def test_encrypt_xor_long_data() -> None:
    """
    Test case 6: Encrypt long data string.
    """
    # Arrange
    data = (
        "This is a very long message that spans multiple lines and contains lots of text to test the XOR encryption with longer content. "
        * 10
    )
    key = "testkey"

    # Act
    encrypted, returned_key = encrypt_xor(data, key=key)

    # Assert
    assert isinstance(encrypted, str)
    assert returned_key == key
    assert (
        len(encrypted) == len(data.encode("utf-8")) * 2
    )  # Hex representation doubles length
    assert all(c in "0123456789abcdef" for c in encrypted)


def test_encrypt_xor_key_length_adaptation() -> None:
    """
    Test case 7: Verify key length adaptation based on data size.
    """
    # Arrange
    short_data = "Hi"
    long_data = "This is a much longer message for testing key length adaptation"

    # Act
    _, short_key = encrypt_xor(short_data)
    _, long_key = encrypt_xor(long_data)

    # Assert
    assert len(short_key) >= 8  # Minimum key length
    # Both should be reasonable lengths
    assert len(short_key) > 0
    assert len(long_key) > 0


def test_encrypt_xor_deterministic_with_same_key() -> None:
    """
    Test case 8: Same data and key should produce same encrypted result.
    """
    # Arrange
    data = "Consistent data"
    key = "consistent_key"

    # Act
    encrypted1, _ = encrypt_xor(data, key=key)
    encrypted2, _ = encrypt_xor(data, key=key)

    # Assert
    assert encrypted1 == encrypted2


def test_encrypt_xor_special_characters() -> None:
    """
    Test case 9: Handle special characters and symbols.
    """
    # Arrange
    data = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
    key = "special"

    # Act
    encrypted, returned_key = encrypt_xor(data, key=key)

    # Assert
    assert isinstance(encrypted, str)
    assert returned_key == key
    assert len(encrypted) > 0
    assert all(c in "0123456789abcdef" for c in encrypted)


def test_encrypt_xor_empty_data_raises_error() -> None:
    """
    Test case 10: Empty data should raise ValueError.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="data cannot be empty"):
        encrypt_xor("")


def test_encrypt_xor_type_validation() -> None:
    """
    Test case 11: Type validation for parameters.
    """
    # Test invalid data type
    with pytest.raises(TypeError, match="data must be a string"):
        encrypt_xor(123)

    # Test invalid key type
    with pytest.raises(TypeError, match="key must be a string or None"):
        encrypt_xor("data", key=123)


def test_encrypt_xor_empty_key_raises_error() -> None:
    """
    Test case 12: Empty key should raise ValueError.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="key cannot be empty"):
        encrypt_xor("data", key="")
