"""
Unit tests for decrypt_xor function.
"""

import pytest
from security_functions.encryption_helpers.encrypt_xor import encrypt_xor
from security_functions.encryption_helpers.decrypt_xor import decrypt_xor


def test_decrypt_xor_case_1_basic_decryption() -> None:
    """
    Test case 1: Basic XOR decryption should recover original data.
    """
    # Arrange
    original_data = "Hello, World!"
    encrypted, key = encrypt_xor(original_data)

    # Act
    decrypted = decrypt_xor(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_xor_case_2_custom_key_decryption() -> None:
    """
    Test case 2: Decrypt data encrypted with custom key.
    """
    # Arrange
    original_data = "Test message with custom key"
    custom_key = "mycustomkey"
    encrypted, _ = encrypt_xor(original_data, key=custom_key)

    # Act
    decrypted = decrypt_xor(encrypted, custom_key)

    # Assert
    assert decrypted == original_data


def test_decrypt_xor_case_3_type_validation() -> None:
    """
    Test case 3: Type validation for parameters.
    """
    # Test invalid encrypted_data type
    with pytest.raises(TypeError, match="encrypted_data must be a string"):
        decrypt_xor(123, "key")

    # Test invalid key type
    with pytest.raises(TypeError, match="key must be a string"):
        decrypt_xor("encrypted", 123)


def test_decrypt_xor_case_4_value_validation() -> None:
    """
    Test case 4: Value validation for parameters.
    """
    # Test empty encrypted_data
    with pytest.raises(ValueError, match="encrypted_data cannot be empty"):
        decrypt_xor("", "key")

    # Test empty key
    with pytest.raises(ValueError, match="key cannot be empty"):
        decrypt_xor("encrypted", "")


def test_decrypt_xor_case_5_invalid_hex_format() -> None:
    """
    Test case 5: Invalid hex format should raise ValueError.
    """
    # Test odd length hex
    with pytest.raises(ValueError, match="encrypted_data must have even length"):
        decrypt_xor("abc", "key")  # Odd length

    # Test invalid hex characters
    with pytest.raises(ValueError, match="encrypted_data must be valid hex string"):
        decrypt_xor("gggg", "key")  # Invalid hex characters


def test_decrypt_xor_case_6_wrong_key_different_result() -> None:
    """
    Test case 6: Wrong key should produce different (incorrect) result.
    """
    # Arrange
    original_data = "Secret message"
    correct_key = "correct_key"
    wrong_key = "wrong_key"
    encrypted, _ = encrypt_xor(original_data, key=correct_key)

    # Act
    correct_decrypted = decrypt_xor(encrypted, correct_key)
    wrong_decrypted = decrypt_xor(encrypted, wrong_key)

    # Assert
    assert correct_decrypted == original_data
    assert wrong_decrypted != original_data


def test_decrypt_xor_case_7_unicode_data() -> None:
    """
    Test case 7: Handle Unicode characters in data.
    """
    # Arrange
    original_data = "Hello 世界! 🌍 ümläuts"
    encrypted, key = encrypt_xor(original_data)

    # Act
    decrypted = decrypt_xor(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_xor_case_8_long_data() -> None:
    """
    Test case 8: Decrypt long data string.
    """
    # Arrange
    original_data = (
        "This is a very long message that spans multiple lines and contains lots of text to test the XOR decryption with longer content. "
        * 10
    )
    key = "testkey"
    encrypted, _ = encrypt_xor(original_data, key=key)

    # Act
    decrypted = decrypt_xor(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_xor_case_9_special_characters() -> None:
    """
    Test case 9: Handle special characters and symbols.
    """
    # Arrange
    original_data = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
    key = "special"
    encrypted, _ = encrypt_xor(original_data, key=key)

    # Act
    decrypted = decrypt_xor(encrypted, key)

    # Assert
    assert decrypted == original_data


def test_decrypt_xor_case_10_empty_original_data() -> None:
    """
    Test case 10: Handle empty string encryption/decryption.
    """
    # Note: This test is for edge case documentation
    # The encrypt_xor function doesn't allow empty data, so this tests
    # the theoretical case where someone manually creates an empty hex string

    # Arrange - manually create "encrypted" empty data
    encrypted_empty = ""  # Empty hex string
    key = "somekey"

    # Act & Assert
    with pytest.raises(ValueError, match="encrypted_data cannot be empty"):
        decrypt_xor(encrypted_empty, key)


def test_decrypt_xor_case_11_roundtrip_multiple_times() -> None:
    """
    Test case 11: Multiple encrypt/decrypt roundtrips should be consistent.
    """
    # Arrange
    original_data = "Roundtrip test data"
    key = "roundtrip_key"

    # Act - Multiple roundtrips
    encrypted1, _ = encrypt_xor(original_data, key=key)
    decrypted1 = decrypt_xor(encrypted1, key)

    encrypted2, _ = encrypt_xor(decrypted1, key=key)
    decrypted2 = decrypt_xor(encrypted2, key)

    # Assert
    assert decrypted1 == original_data
    assert decrypted2 == original_data
    assert encrypted1 == encrypted2  # Should be deterministic


def test_decrypt_xor_case_12_case_sensitive_hex() -> None:
    """
    Test case 12: Hex decryption should handle both uppercase and lowercase.
    """
    # Arrange
    original_data = "Case test"
    key = "testkey"
    encrypted, _ = encrypt_xor(original_data, key=key)

    # Convert to uppercase
    encrypted_upper = encrypted.upper()

    # Act
    decrypted_lower = decrypt_xor(encrypted, key)
    decrypted_upper = decrypt_xor(encrypted_upper, key)

    # Assert
    assert decrypted_lower == original_data
    assert decrypted_upper == original_data
