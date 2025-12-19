import pytest
from security_functions.password_hashing.hash_password_pbkdf2 import (
    hash_password_pbkdf2,
)


def test_hash_password_pbkdf2_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid password.
    """
    # Arrange
    password = "my_secret_password"

    # Act
    hashed, salt = hash_password_pbkdf2(password)

    # Assert
    assert isinstance(hashed, str)
    assert isinstance(salt, bytes)
    assert len(hashed) == 64  # SHA-256 hex string length
    assert len(salt) == 32  # Default salt length
    assert all(c in "0123456789abcdef" for c in hashed)


def test_hash_password_pbkdf2_custom_salt() -> None:
    """
    Test case 2: Using custom salt.
    """
    # Arrange
    password = "test_password"
    custom_salt = b"this_is_a_32_byte_salt_value__"

    # Act
    hashed, returned_salt = hash_password_pbkdf2(password, salt=custom_salt)

    # Assert
    assert isinstance(hashed, str)
    assert returned_salt == custom_salt
    assert len(hashed) == 64


def test_hash_password_pbkdf2_custom_iterations() -> None:
    """
    Test case 3: Using custom iteration count.
    """
    # Arrange
    password = "test_password"
    iterations = 50000

    # Act
    hashed, salt = hash_password_pbkdf2(password, iterations=iterations)

    # Assert
    assert isinstance(hashed, str)
    assert isinstance(salt, bytes)
    assert len(hashed) == 64
    assert len(salt) == 32


def test_hash_password_pbkdf2_deterministic_with_same_salt() -> None:
    """
    Test case 4: Same password and salt should produce same hash.
    """
    # Arrange
    password = "consistent_password"
    salt = b"consistent_salt_32_bytes_here__"

    # Act
    hashed1, _ = hash_password_pbkdf2(password, salt=salt)
    hashed2, _ = hash_password_pbkdf2(password, salt=salt)

    # Assert
    assert hashed1 == hashed2


def test_hash_password_pbkdf2_different_passwords_different_hashes() -> None:
    """
    Test case 5: Different passwords should produce different hashes.
    """
    # Arrange
    password1 = "password1"
    password2 = "password2"
    salt = b"same_salt_for_both_passwords___"

    # Act
    hashed1, _ = hash_password_pbkdf2(password1, salt=salt)
    hashed2, _ = hash_password_pbkdf2(password2, salt=salt)

    # Assert
    assert hashed1 != hashed2


def test_hash_password_pbkdf2_random_salt_generation() -> None:
    """
    Test case 6: Random salt generation produces different salts.
    """
    # Arrange
    password = "same_password"

    # Act
    _, salt1 = hash_password_pbkdf2(password)
    _, salt2 = hash_password_pbkdf2(password)

    # Assert
    assert salt1 != salt2
    assert len(salt1) == 32
    assert len(salt2) == 32


def test_hash_password_pbkdf2_unicode_password() -> None:
    """
    Test case 7: Handle Unicode characters in password.
    """
    # Arrange
    password = "pássw0rd_with_ümläuts_🔐"

    # Act
    hashed, salt = hash_password_pbkdf2(password)

    # Assert
    assert isinstance(hashed, str)
    assert isinstance(salt, bytes)
    assert len(hashed) == 64
    assert len(salt) == 32


def test_hash_password_pbkdf2_boundary_iterations() -> None:
    """
    Test case 8: Test boundary values for iterations.
    """
    # Arrange
    password = "test_password"

    # Test minimum valid iterations
    hashed_min, salt_min = hash_password_pbkdf2(password, iterations=1000)
    assert len(hashed_min) == 64

    # Test high iterations
    hashed_high, salt_high = hash_password_pbkdf2(password, iterations=200000)
    assert len(hashed_high) == 64


def test_hash_password_pbkdf2_type_validation() -> None:
    """
    Test case 9: Type validation for all parameters.
    """
    # Test invalid password type
    with pytest.raises(TypeError, match="password must be a string"):
        hash_password_pbkdf2(123)

    # Test invalid salt type
    with pytest.raises(TypeError, match="salt must be bytes or None"):
        hash_password_pbkdf2("password", salt="invalid")

    # Test invalid iterations type
    with pytest.raises(TypeError, match="iterations must be an integer"):
        hash_password_pbkdf2("password", iterations="invalid")


def test_hash_password_pbkdf2_value_validation() -> None:
    """
    Test case 10: Value validation for parameters.
    """
    # Test empty password
    with pytest.raises(ValueError, match="password cannot be empty"):
        hash_password_pbkdf2("")

    # Test too few iterations
    with pytest.raises(ValueError, match="iterations must be at least 1000"):
        hash_password_pbkdf2("password", iterations=500)
