import pytest

try:
    from cryptography.fernet import Fernet
    from pyutils_collection.security_functions.token_generation.generate_url_safe_token import (
        generate_url_safe_token,
    )
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    Fernet = None  # type: ignore
    generate_url_safe_token = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.security,
    pytest.mark.skipif(not CRYPTOGRAPHY_AVAILABLE, reason="cryptography not installed"),
]


def test_generate_url_safe_token_default_length() -> None:
    """
    Test case 1: Generate token with default length.
    """
    # Act
    token = generate_url_safe_token()

    # Assert
    assert isinstance(token, str)
    assert len(token) >= 16  # Should be at least close to requested length
    assert all(c.isalnum() or c in "-_" for c in token)  # URL-safe characters only


def test_generate_url_safe_token_custom_length() -> None:
    """
    Test case 2: Generate token with custom length.
    """
    # Arrange
    length = 16

    # Act
    token = generate_url_safe_token(length=length)

    # Assert
    assert isinstance(token, str)
    assert len(token) >= 16  # Should be at least the requested length
    assert all(c.isalnum() or c in "-_" for c in token)


def test_generate_url_safe_token_short_length() -> None:
    """
    Test case 3: Generate token with short length.
    """
    # Arrange
    length = 8

    # Act
    token = generate_url_safe_token(length=length)

    # Assert
    assert isinstance(token, str)
    assert len(token) >= 8
    assert all(c.isalnum() or c in "-_" for c in token)


def test_generate_url_safe_token_long_length() -> None:
    """
    Test case 4: Generate token with long length.
    """
    # Arrange
    length = 128

    # Act
    token = generate_url_safe_token(length=length)

    # Assert
    assert isinstance(token, str)
    assert len(token) >= 128
    assert all(c.isalnum() or c in "-_" for c in token)


def test_generate_url_safe_token_randomness() -> None:
    """
    Test case 5: Generated tokens should be different (randomness).
    """
    # Act
    token1 = generate_url_safe_token()
    token2 = generate_url_safe_token()
    token3 = generate_url_safe_token()

    # Assert
    assert token1 != token2
    assert token2 != token3
    assert token1 != token3


def test_generate_url_safe_token_url_safe_characters() -> None:
    """
    Test case 6: Verify only URL-safe characters are used.
    """
    # Act
    token = generate_url_safe_token(length=100)  # Larger token for better coverage

    # Assert
    assert isinstance(token, str)
    # Should only contain alphanumeric characters, hyphens, and underscores
    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    )
    token_chars = set(token)
    assert token_chars.issubset(allowed_chars)


def test_generate_url_safe_token_no_padding() -> None:
    """
    Test case 7: Verify that no base64 padding characters are present.
    """
    # Act
    token = generate_url_safe_token(length=50)

    # Assert
    assert isinstance(token, str)
    assert "=" not in token  # No padding characters


def test_generate_url_safe_token_minimum_length() -> None:
    """
    Test case 8: Test minimum valid length.
    """
    # Act
    token = generate_url_safe_token(length=1)

    # Assert
    assert isinstance(token, str)
    assert len(token) >= 1
    assert all(c.isalnum() or c in "-_" for c in token)


def test_generate_url_safe_token_consistent_character_set() -> None:
    """
    Test case 9: Verify consistent character set across multiple generations.
    """
    # Act - Generate multiple tokens
    tokens = [generate_url_safe_token(length=50) for _ in range(10)]

    # Assert
    all_chars = set()
    for token in tokens:
        all_chars.update(set(token))

    # All characters should be URL-safe
    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    )
    assert all_chars.issubset(allowed_chars)


def test_generate_url_safe_token_base64_properties() -> None:
    """
    Test case 10: Verify properties inherited from base64 encoding.
    """
    # Act
    token = generate_url_safe_token(length=32)

    # Assert
    assert isinstance(token, str)
    # Should be at least the requested length
    assert len(token) >= 32
    # Should not contain characters that need URL encoding
    forbidden_chars = set("+/=")  # Standard base64 chars that are not URL-safe
    assert not any(char in forbidden_chars for char in token)


def test_generate_url_safe_token_type_validation() -> None:
    """
    Test case 11: Type validation for length parameter.
    """
    # Test invalid length type
    with pytest.raises(TypeError, match="length must be an integer"):
        generate_url_safe_token(length="invalid")


def test_generate_url_safe_token_value_validation() -> None:
    """
    Test case 12: Value validation for length parameter.
    """
    # Test length less than 1
    with pytest.raises(ValueError, match="length must be at least 1"):
        generate_url_safe_token(length=0)

    with pytest.raises(ValueError, match="length must be at least 1"):
        generate_url_safe_token(length=-1)
