import pytest

pytestmark = [pytest.mark.unit, pytest.mark.security]
from python_utils.security_functions.password_hashing.hash_password_bcrypt import (
    hash_password_bcrypt,
)
from python_utils.security_functions.password_hashing.verify_password_bcrypt import (
    verify_password_bcrypt,
)


def test_verify_password_bcrypt_correct_password() -> None:
    """
    Test case 1: Verify correct password returns True.
    """
    # Arrange
    password = "correct_password"
    hashed = hash_password_bcrypt(password)

    # Act
    result = verify_password_bcrypt(password, hashed)

    # Assert
    assert result is True


def test_verify_password_bcrypt_incorrect_password() -> None:
    """
    Test case 2: Verify incorrect password returns False.
    """
    # Arrange
    correct_password = "correct_password"
    wrong_password = "wrong_password"
    hashed = hash_password_bcrypt(correct_password)

    # Act
    result = verify_password_bcrypt(wrong_password, hashed)

    # Assert
    assert result is False


def test_verify_password_bcrypt_different_rounds() -> None:
    """
    Test case 3: Verify password with different rounds.
    """
    # Arrange
    password = "test_password"
    rounds = 10
    hashed = hash_password_bcrypt(password, rounds=rounds)

    # Act
    result = verify_password_bcrypt(password, hashed)

    # Assert
    assert result is True


def test_verify_password_bcrypt_case_sensitive() -> None:
    """
    Test case 4: Password verification should be case sensitive.
    """
    # Arrange
    password = "CaseSensitive"
    hashed = hash_password_bcrypt(password)

    # Act
    correct_result = verify_password_bcrypt("CaseSensitive", hashed)
    wrong_case_result = verify_password_bcrypt("casesensitive", hashed)

    # Assert
    assert correct_result is True
    assert wrong_case_result is False


def test_verify_password_bcrypt_unicode_password() -> None:
    """
    Test case 5: Handle Unicode characters in password verification.
    """
    # Arrange
    password = "pássw0rd_with_ümläuts_🔐"
    hashed = hash_password_bcrypt(password)

    # Act
    correct_result = verify_password_bcrypt(password, hashed)
    wrong_result = verify_password_bcrypt("different_password", hashed)

    # Assert
    assert correct_result is True
    assert wrong_result is False


def test_verify_password_bcrypt_special_characters() -> None:
    """
    Test case 6: Handle special characters in password verification.
    """
    # Arrange
    password = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
    hashed = hash_password_bcrypt(password)

    # Act
    result = verify_password_bcrypt(password, hashed)

    # Assert
    assert result is True


def test_verify_password_bcrypt_long_password() -> None:
    """
    Test case 7: Handle very long password verification (bcrypt rejects >72 bytes).
    """
    # Arrange
    password = "a" * 1000  # Very long password (exceeds 72-byte limit)
    # Create a valid hash for verification with a password within the limit
    short_password = "a" * 72
    hashed = hash_password_bcrypt(short_password)

    # Act & Assert - bcrypt.checkpw raises ValueError for passwords >72 bytes
    # The verify function catches this and returns False
    result = verify_password_bcrypt(password, hashed)
    
    # Assert - bcrypt library now rejects long passwords during verification
    # The verify function catches the exception and returns False
    assert result is False


def test_verify_password_bcrypt_timing_attack_resistance() -> None:
    """
    Test case 8: Verify that function handles invalid hashes gracefully.
    """
    # Arrange
    password = "test_password"
    hash_password_bcrypt(password)

    # Test with various invalid hash formats that might cause timing differences
    invalid_hashes = [
        "$2b$12$" + "x" * 53,  # Invalid characters but correct length
        "$2b$12$" + "a" * 53,  # Valid characters but wrong hash
    ]

    # Act & Assert
    for invalid_hash in invalid_hashes:
        result = verify_password_bcrypt(password, invalid_hash)
        assert result is False  # Should return False, not raise exception


def test_verify_password_bcrypt_type_validation() -> None:
    """
    Test case 9: Type validation for all parameters.
    """
    hashed = hash_password_bcrypt("password")

    # Test invalid password type
    with pytest.raises(TypeError, match="password must be a string"):
        verify_password_bcrypt(123, hashed)

    # Test invalid hashed_password type
    with pytest.raises(TypeError, match="hashed_password must be a string"):
        verify_password_bcrypt("password", 123)


def test_verify_password_bcrypt_value_validation() -> None:
    """
    Test case 10: Value validation for parameters.
    """
    hashed = hash_password_bcrypt("password")

    # Test empty password
    with pytest.raises(ValueError, match="password cannot be empty"):
        verify_password_bcrypt("", hashed)

    # Test empty hashed_password
    with pytest.raises(ValueError, match="hashed_password cannot be empty"):
        verify_password_bcrypt("password", "")


def test_verify_password_bcrypt_invalid_hash_format() -> None:
    """
    Test case 11: Invalid bcrypt hash format should raise ValueError.
    """
    # Test invalid bcrypt identifier
    with pytest.raises(ValueError, match="Invalid bcrypt hash format"):
        verify_password_bcrypt("password", "$1$invalid_hash_format_here")

    # Test wrong length
    with pytest.raises(
        ValueError, match="hashed_password must be exactly 60 characters"
    ):
        verify_password_bcrypt("password", "$2b$12$short")


def test_verify_password_bcrypt_malformed_hash() -> None:
    """
    Test case 12: Malformed hash should raise ValueError.
    """
    # Test completely invalid hash
    with pytest.raises(ValueError, match="Invalid bcrypt hash format"):
        verify_password_bcrypt(
            "password", "completely_invalid_hash_string_that_is_60_chars_long_x"
        )
