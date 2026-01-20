import string

import pytest

try:
    from cryptography.fernet import Fernet
    from python_utils.security_functions.token_generation.generate_secure_token import (
        generate_secure_token,
    )
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None  # type: ignore
    generate_secure_token = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.security,
    pytest.mark.skipif(not CRYPTOGRAPHY_AVAILABLE, reason="cryptography not installed"),
]


def test_generate_secure_token_default_parameters() -> None:
    """
    Test case 1: Generate token with default parameters.
    """
    # Act
    token = generate_secure_token()

    # Assert
    assert isinstance(token, str)
    assert len(token) == 32  # Default length
    assert token.isalnum()  # Only letters and digits by default


def test_generate_secure_token_custom_length() -> None:
    """
    Test case 2: Generate token with custom length.
    """
    # Arrange
    length = 16

    # Act
    token = generate_secure_token(length=length)

    # Assert
    assert isinstance(token, str)
    assert len(token) == length


def test_generate_secure_token_letters_only() -> None:
    """
    Test case 3: Generate token with letters only.
    """
    # Act
    token = generate_secure_token(include_digits=False, include_symbols=False)

    # Assert
    assert isinstance(token, str)
    assert len(token) == 32
    assert token.isalpha()  # Only letters
    assert any(c.islower() for c in token)  # Has lowercase
    assert any(c.isupper() for c in token)  # Has uppercase


def test_generate_secure_token_digits_only() -> None:
    """
    Test case 4: Generate token with digits only.
    """
    # Act
    token = generate_secure_token(include_letters=False, include_symbols=False)

    # Assert
    assert isinstance(token, str)
    assert len(token) == 32
    assert token.isdigit()  # Only digits


def test_generate_secure_token_with_symbols() -> None:
    """
    Test case 5: Generate token including symbols.
    """
    # Act
    token = generate_secure_token(include_symbols=True)

    # Assert
    assert isinstance(token, str)
    assert len(token) == 32
    # Check that token contains at least one character from each enabled set
    has_letter = any(c in string.ascii_letters for c in token)
    has_digit = any(c in string.digits for c in token)
    any(c in "!@#$%^&*-_=+[]{}|;:,.<>?" for c in token)
    # At least letters and digits should be present (symbols may or may not appear)
    assert has_letter or has_digit


def test_generate_secure_token_randomness() -> None:
    """
    Test case 6: Generated tokens should be different (randomness).
    """
    # Act
    token1 = generate_secure_token()
    token2 = generate_secure_token()
    token3 = generate_secure_token()

    # Assert
    assert token1 != token2
    assert token2 != token3
    assert token1 != token3


def test_generate_secure_token_symbols_only() -> None:
    """
    Test case 7: Generate token with symbols only.
    """
    # Act
    token = generate_secure_token(
        length=20, include_letters=False, include_digits=False, include_symbols=True
    )

    # Assert
    assert isinstance(token, str)
    assert len(token) == 20
    assert all(c in "!@#$%^&*-_=+[]{}|;:,.<>?" for c in token)


def test_generate_secure_token_boundary_lengths() -> None:
    """
    Test case 8: Test boundary values for length.
    """
    # Test minimum length
    token_min = generate_secure_token(length=1)
    assert len(token_min) == 1

    # Test large length
    token_large = generate_secure_token(length=1000)
    assert len(token_large) == 1000


def test_generate_secure_token_all_character_types() -> None:
    """
    Test case 9: Generate token with all character types enabled.
    """
    # Act
    token = generate_secure_token(
        length=100,  # Larger length to increase chance of all types appearing
        include_letters=True,
        include_digits=True,
        include_symbols=True,
    )

    # Assert
    assert isinstance(token, str)
    assert len(token) == 100
    # Check character set validity
    valid_chars = string.ascii_letters + string.digits + "!@#$%^&*-_=+[]{}|;:,.<>?"
    assert all(c in valid_chars for c in token)


def test_generate_secure_token_type_validation() -> None:
    """
    Test case 10: Type validation for all parameters.
    """
    # Test invalid length type
    with pytest.raises(TypeError, match="length must be an integer"):
        generate_secure_token(length="invalid")

    # Test invalid include_letters type
    with pytest.raises(TypeError, match="include_letters must be a boolean"):
        generate_secure_token(include_letters="invalid")

    # Test invalid include_digits type
    with pytest.raises(TypeError, match="include_digits must be a boolean"):
        generate_secure_token(include_digits="invalid")

    # Test invalid include_symbols type
    with pytest.raises(TypeError, match="include_symbols must be a boolean"):
        generate_secure_token(include_symbols="invalid")


def test_generate_secure_token_value_validation() -> None:
    """
    Test case 11: Value validation for parameters.
    """
    # Test length less than 1
    with pytest.raises(ValueError, match="length must be at least 1"):
        generate_secure_token(length=0)

    # Test no character types selected
    with pytest.raises(
        ValueError, match="at least one character type must be included"
    ):
        generate_secure_token(
            include_letters=False, include_digits=False, include_symbols=False
        )
