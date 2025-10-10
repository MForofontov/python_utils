import pytest
from security_functions.password_hashing.hash_password_pbkdf2 import (
    hash_password_pbkdf2,
)
from security_functions.password_hashing.verify_password_pbkdf2 import (
    verify_password_pbkdf2,
)


def test_verify_password_pbkdf2_case_1_correct_password() -> None:
    """
    Test case 1: Verify correct password returns True.
    """
    # Arrange
    password = "my_secret_password"
    hashed, salt = hash_password_pbkdf2(password)

    # Act
    result = verify_password_pbkdf2(password, hashed, salt)

    # Assert
    assert result is True


def test_verify_password_pbkdf2_case_2_incorrect_password() -> None:
    """
    Test case 2: Verify incorrect password returns False.
    """
    # Arrange
    correct_password = "correct_password"
    wrong_password = "wrong_password"
    hashed, salt = hash_password_pbkdf2(correct_password)

    # Act
    result = verify_password_pbkdf2(wrong_password, hashed, salt)

    # Assert
    assert result is False


def test_verify_password_pbkdf2_case_3_custom_iterations() -> None:
    """
    Test case 3: Verify with custom iteration count.
    """
    # Arrange
    password = "test_password"
    iterations = 50000
    hashed, salt = hash_password_pbkdf2(password, iterations=iterations)

    # Act
    result = verify_password_pbkdf2(password, hashed, salt, iterations=iterations)

    # Assert
    assert result is True


def test_verify_password_pbkdf2_case_7_different_iterations() -> None:
    """
    Test case 4: Verification fails with different iteration count.
    """
    # Arrange
    password = "test_password"
    hashed, salt = hash_password_pbkdf2(password, iterations=10000)

    # Act
    result = verify_password_pbkdf2(password, hashed, salt, iterations=20000)

    # Assert
    assert result is False


def test_verify_password_pbkdf2_case_8_unicode_password() -> None:
    """
    Test case 5: Handle Unicode characters in password verification.
    """
    # Arrange
    password = "pássw0rd_with_ümläuts_🔐"
    hashed, salt = hash_password_pbkdf2(password)

    # Act
    result = verify_password_pbkdf2(password, hashed, salt)

    # Assert
    assert result is True


def test_verify_password_pbkdf2_case_9_case_sensitive() -> None:
    """
    Test case 6: Password verification is case sensitive.
    """
    # Arrange
    password = "CaseSensitivePassword"
    hashed, salt = hash_password_pbkdf2(password)
    wrong_case = "casesensitivepassword"

    # Act
    result_correct = verify_password_pbkdf2(password, hashed, salt)
    result_wrong_case = verify_password_pbkdf2(wrong_case, hashed, salt)

    # Assert
    assert result_correct is True
    assert result_wrong_case is False


def test_verify_password_pbkdf2_case_10_edge_case_similar_passwords() -> None:
    """
    Test case 7: Verification with very similar but different passwords.
    """
    # Arrange
    password1 = "password123"
    password2 = "password124"  # Only last character different
    hashed, salt = hash_password_pbkdf2(password1)

    # Act
    result1 = verify_password_pbkdf2(password1, hashed, salt)
    result2 = verify_password_pbkdf2(password2, hashed, salt)

    # Assert
    assert result1 is True
    assert result2 is False
def test_verify_password_pbkdf2_case_4_type_validation() -> None:
    """
    Test case 8: Type validation for all parameters.
    """
    # Arrange
    hashed, salt = hash_password_pbkdf2("password")

    # Test invalid password type
    with pytest.raises(TypeError, match="password must be a string"):
        verify_password_pbkdf2(123, hashed, salt)

    # Test invalid hashed_password type
    with pytest.raises(TypeError, match="hashed_password must be a string"):
        verify_password_pbkdf2("password", 123, salt)

    # Test invalid salt type
    with pytest.raises(TypeError, match="salt must be bytes"):
        verify_password_pbkdf2("password", hashed, "invalid")

    # Test invalid iterations type
    with pytest.raises(TypeError, match="iterations must be an integer"):
        verify_password_pbkdf2("password", hashed, salt, iterations="invalid")


def test_verify_password_pbkdf2_case_5_value_validation() -> None:
    """
    Test case 9: Value validation for parameters.
    """
    # Arrange
    hashed, salt = hash_password_pbkdf2("password")

    # Test empty password
    with pytest.raises(ValueError, match="password cannot be empty"):
        verify_password_pbkdf2("", hashed, salt)

    # Test empty hashed_password
    with pytest.raises(ValueError, match="hashed_password cannot be empty"):
        verify_password_pbkdf2("password", "", salt)

    # Test empty salt
    with pytest.raises(ValueError, match="salt cannot be empty"):
        verify_password_pbkdf2("password", hashed, b"")

    # Test too few iterations
    with pytest.raises(ValueError, match="iterations must be at least 1000"):
        verify_password_pbkdf2("password", hashed, salt, iterations=500)


def test_verify_password_pbkdf2_case_6_invalid_hex_format() -> None:
    """
    Test case 10: Invalid hex format in hashed_password.
    """
    # Arrange
    password = "test_password"
    _, salt = hash_password_pbkdf2(password)
    invalid_hex = "not_valid_hex"

    # Act & Assert
    with pytest.raises(ValueError, match="hashed_password must be a valid hex string"):
        verify_password_pbkdf2(password, invalid_hex, salt)
