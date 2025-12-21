"""
Tests for slugify_url function.
"""

import pytest

from url_functions.slugify_url import slugify_url


def test_slugify_url_basic_text() -> None:
    """
    Test case 1: Basic text with spaces and punctuation.
    """
    # Arrange
    text = "Hello World!"
    expected = "hello-world"

    # Act
    result = slugify_url(text)

    # Assert
    assert result == expected


def test_slugify_url_with_special_characters() -> None:
    """
    Test case 2: Text with special characters and numbers.
    """
    # Arrange
    text = "Python 3.11: New Features & Benefits"
    expected = "python-311-new-features-benefits"

    # Act
    result = slugify_url(text)

    # Assert
    assert result == expected


def test_slugify_url_with_unicode() -> None:
    """
    Test case 3: Unicode text with allow_unicode=True.
    """
    # Arrange
    text = "Café & Restaurant"
    expected = "café-restaurant"

    # Act
    result = slugify_url(text, allow_unicode=True)

    # Assert
    assert result == expected


def test_slugify_url_unicode_to_ascii() -> None:
    """
    Test case 4: Unicode text converted to ASCII (default).
    """
    # Arrange
    text = "Café & Restaurant"
    expected = "cafe-restaurant"

    # Act
    result = slugify_url(text, allow_unicode=False)

    # Assert
    assert result == expected


def test_slugify_url_max_length() -> None:
    """
    Test case 5: Long text with max_length constraint.
    """
    # Arrange
    text = "This is a very long title that should be truncated"
    max_length = 15
    expected = "this-is-a-very"

    # Act
    result = slugify_url(text, max_length=max_length)

    # Assert
    assert result == expected
    assert len(result) <= max_length


def test_slugify_url_custom_separator() -> None:
    """
    Test case 6: Custom separator instead of hyphen.
    """
    # Arrange
    text = "Hello World Test"
    expected = "hello_world_test"

    # Act
    result = slugify_url(text, separator="_")

    # Assert
    assert result == expected


def test_slugify_url_uppercase() -> None:
    """
    Test case 7: Keep uppercase with lowercase=False.
    """
    # Arrange
    text = "Hello World"
    expected = "Hello-World"

    # Act
    result = slugify_url(text, lowercase=False)

    # Assert
    assert result == expected


def test_slugify_url_multiple_spaces() -> None:
    """
    Test case 8: Multiple consecutive spaces collapsed.
    """
    # Arrange
    text = "Hello    World    Test"
    expected = "hello-world-test"

    # Act
    result = slugify_url(text)

    # Assert
    assert result == expected


def test_slugify_url_leading_trailing_spaces() -> None:
    """
    Test case 9: Leading and trailing spaces removed.
    """
    # Arrange
    text = "   Hello World   "
    expected = "hello-world"

    # Act
    result = slugify_url(text)

    # Assert
    assert result == expected


def test_slugify_url_empty_string_raises_error() -> None:
    """
    Test case 10: ValueError for empty string.
    """
    # Arrange
    text = ""
    expected_message = "text cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        slugify_url(text)


def test_slugify_url_invalid_type_raises_error() -> None:
    """
    Test case 11: TypeError for non-string input.
    """
    # Arrange
    text = 123
    expected_message = "text must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        slugify_url(text)  # type: ignore


def test_slugify_url_negative_max_length_raises_error() -> None:
    """
    Test case 12: ValueError for negative max_length.
    """
    # Arrange
    text = "Hello World"
    max_length = -1
    expected_message = "max_length must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        slugify_url(text, max_length=max_length)


def test_slugify_url_empty_separator_raises_error() -> None:
    """
    Test case 13: ValueError for empty separator.
    """
    # Arrange
    text = "Hello World"
    separator = ""
    expected_message = "separator cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        slugify_url(text, separator=separator)


def test_slugify_url_only_special_characters() -> None:
    """
    Test case 14: Text with only special characters returns empty.
    """
    # Arrange
    text = "!@#$%^&*()"
    expected = ""

    # Act
    result = slugify_url(text)

    # Assert
    assert result == expected


def test_slugify_url_consecutive_hyphens() -> None:
    """
    Test case 15: Consecutive hyphens collapsed to single hyphen.
    """
    # Arrange
    text = "Hello---World"
    expected = "hello-world"

    # Act
    result = slugify_url(text)

    # Assert
    assert result == expected
