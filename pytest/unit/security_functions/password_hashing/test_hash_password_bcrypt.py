import pytest

pytestmark = [pytest.mark.unit, pytest.mark.security]
from security_functions.password_hashing.hash_password_bcrypt import (
    hash_password_bcrypt,
)


def test_hash_password_bcrypt_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid password.
    """
    # Arrange
    password = "my_secret_password"

    # Act
    hashed = hash_password_bcrypt(password)

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60  # bcrypt hashes are always 60 characters
    assert hashed.startswith("$2b$")  # bcrypt identifier


def test_hash_password_bcrypt_custom_rounds() -> None:
    """
    Test case 2: Using custom rounds parameter.
    """
    # Arrange
    password = "test_password"
    rounds = 10

    # Act
    hashed = hash_password_bcrypt(password, rounds=rounds)

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60
    assert f"$2b${rounds:02d}$" in hashed  # Should contain the round number


def test_hash_password_bcrypt_minimum_rounds() -> None:
    """
    Test case 3: Using minimum valid rounds.
    """
    # Arrange
    password = "test_password"
    rounds = 4

    # Act
    hashed = hash_password_bcrypt(password, rounds=rounds)

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60
    assert "$2b$04$" in hashed


def test_hash_password_bcrypt_maximum_rounds() -> None:
    """
    Test case 4: Using maximum valid rounds (reduced for testing performance).
    """
    # Arrange
    password = "test_password"
    rounds = 15  # Use 15 instead of 31 for reasonable test performance

    # Act
    hashed = hash_password_bcrypt(password, rounds=rounds)

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60
    assert "$2b$15$" in hashed


def test_hash_password_bcrypt_different_passwords_different_hashes() -> None:
    """
    Test case 5: Different passwords should produce different hashes.
    """
    # Arrange
    password1 = "password1"
    password2 = "password2"

    # Act
    hashed1 = hash_password_bcrypt(password1)
    hashed2 = hash_password_bcrypt(password2)

    # Assert
    assert hashed1 != hashed2


def test_hash_password_bcrypt_same_password_different_hashes() -> None:
    """
    Test case 6: Same password should produce different hashes due to salt.
    """
    # Arrange
    password = "same_password"

    # Act
    hashed1 = hash_password_bcrypt(password)
    hashed2 = hash_password_bcrypt(password)

    # Assert
    assert hashed1 != hashed2  # Different due to random salt


def test_hash_password_bcrypt_unicode_password() -> None:
    """
    Test case 7: Handle Unicode characters in password.
    """
    # Arrange
    password = "pássw0rd_with_ümläuts_🔐"

    # Act
    hashed = hash_password_bcrypt(password)

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60
    assert hashed.startswith("$2b$")


def test_hash_password_bcrypt_long_password() -> None:
    """
    Test case 8: ValueError for password longer than 72 bytes (bcrypt limit).
    """
    # Arrange
    password = "a" * 1000  # Very long password (exceeds 72-byte limit)
    expected_message = "password cannot be longer than 72 bytes"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        hash_password_bcrypt(password)


def test_hash_password_bcrypt_special_characters() -> None:
    """
    Test case 9: Handle special characters and symbols.
    """
    # Arrange
    password = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"

    # Act
    hashed = hash_password_bcrypt(password)

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60
    assert hashed.startswith("$2b$")


def test_hash_password_bcrypt_performance_high_rounds() -> None:
    """
    Test case 10: Verify that higher rounds work (may be slower).
    """
    # Arrange
    password = "performance_test"
    rounds = 15  # Higher but reasonable for testing

    # Act
    import time

    start_time = time.time()
    hashed = hash_password_bcrypt(password, rounds=rounds)
    elapsed_time = time.time() - start_time

    # Assert
    assert isinstance(hashed, str)
    assert len(hashed) == 60
    assert f"$2b${rounds:02d}$" in hashed
    # Should complete within reasonable time (bcrypt with 15 rounds)
    assert elapsed_time < 5.0  # Should complete within 5 seconds


def test_hash_password_bcrypt_type_validation() -> None:
    """
    Test case 11: Type validation for all parameters.
    """
    # Test invalid password type
    with pytest.raises(TypeError, match="password must be a string"):
        hash_password_bcrypt(123)

    # Test invalid rounds type
    with pytest.raises(TypeError, match="rounds must be an integer"):
        hash_password_bcrypt("password", rounds="invalid")


def test_hash_password_bcrypt_value_validation() -> None:
    """
    Test case 12: Value validation for parameters.
    """
    # Test empty password
    with pytest.raises(ValueError, match="password cannot be empty"):
        hash_password_bcrypt("")

    # Test rounds too low
    with pytest.raises(ValueError, match="rounds must be between 4 and 31"):
        hash_password_bcrypt("password", rounds=3)

    # Test rounds too high
    with pytest.raises(ValueError, match="rounds must be between 4 and 31"):
        hash_password_bcrypt("password", rounds=32)
