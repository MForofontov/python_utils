"""
Tests for match_url_pattern and validate_url_format functions.
"""

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.url_functions]
from pyutils_collection.url_functions.match_url_pattern import match_url_pattern, validate_url_format

# Tests for match_url_pattern


def test_match_url_pattern_simple_match() -> None:
    """
    Test case 1: Simple URL pattern match with one variable.
    """
    # Arrange
    url = "/users/123"
    pattern = "/users/{user_id}"
    expected = {"user_id": "123"}

    # Act
    result = match_url_pattern(url, pattern)

    # Assert
    assert result == expected


def test_match_url_pattern_multiple_variables() -> None:
    """
    Test case 2: Pattern with multiple path variables.
    """
    # Arrange
    url = "/users/123/posts/456"
    pattern = "/users/{user_id}/posts/{post_id}"
    expected = {"user_id": "123", "post_id": "456"}

    # Act
    result = match_url_pattern(url, pattern)

    # Assert
    assert result == expected


def test_match_url_pattern_no_match() -> None:
    """
    Test case 3: URL does not match pattern.
    """
    # Arrange
    url = "/products/123"
    pattern = "/users/{user_id}"

    # Act
    result = match_url_pattern(url, pattern)

    # Assert
    assert result is None


def test_match_url_pattern_typed_int() -> None:
    """
    Test case 4: Pattern with int type constraint.
    """
    # Arrange
    url = "/users/123"
    pattern = "/users/{user_id:int}"
    expected = {"user_id": "123"}

    # Act
    result = match_url_pattern(url, pattern)

    # Assert
    assert result == expected


def test_match_url_pattern_typed_int_no_match() -> None:
    """
    Test case 5: Int type constraint fails on non-numeric.
    """
    # Arrange
    url = "/users/abc"
    pattern = "/users/{user_id:int}"

    # Act
    result = match_url_pattern(url, pattern)

    # Assert
    assert result is None


def test_match_url_pattern_path_type() -> None:
    """
    Test case 6: Pattern with path type (multiple segments).
    """
    # Arrange
    url = "/files/docs/user/readme.txt"
    pattern = "/files/{path:path}"
    expected = {"path": "docs/user/readme.txt"}

    # Act
    result = match_url_pattern(url, pattern)

    # Assert
    assert result == expected


def test_match_url_pattern_case_insensitive() -> None:
    """
    Test case 7: Case-insensitive matching (default).
    """
    # Arrange
    url = "/Users/123"
    pattern = "/users/{id}"

    # Act
    result = match_url_pattern(url, pattern, case_sensitive=False)

    # Assert
    assert result is not None
    assert result["id"] == "123"


def test_match_url_pattern_case_sensitive() -> None:
    """
    Test case 8: Case-sensitive matching.
    """
    # Arrange
    url = "/Users/123"
    pattern = "/users/{id}"

    # Act
    result = match_url_pattern(url, pattern, case_sensitive=True)

    # Assert
    assert result is None


def test_match_url_pattern_empty_url_raises_error() -> None:
    """
    Test case 9: ValueError for empty URL.
    """
    # Arrange
    url = ""
    pattern = "/users/{id}"
    expected_message = "url cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        match_url_pattern(url, pattern)


def test_match_url_pattern_empty_pattern_raises_error() -> None:
    """
    Test case 10: ValueError for empty pattern.
    """
    # Arrange
    url = "/users/123"
    pattern = ""
    expected_message = "pattern cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        match_url_pattern(url, pattern)


def test_match_url_pattern_invalid_url_type_raises_error() -> None:
    """
    Test case 11: TypeError for non-string URL.
    """
    # Arrange
    url = 123
    pattern = "/users/{id}"
    expected_message = "url must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        match_url_pattern(url, pattern)  # type: ignore


# Tests for validate_url_format


def test_validate_url_format_valid_https() -> None:
    """
    Test case 12: Valid HTTPS URL.
    """
    # Arrange
    url = "https://example.com/path"

    # Act
    result = validate_url_format(url)

    # Assert
    assert result is True


def test_validate_url_format_valid_http() -> None:
    """
    Test case 13: Valid HTTP URL.
    """
    # Arrange
    url = "http://example.com/path"

    # Act
    result = validate_url_format(url)

    # Assert
    assert result is True


def test_validate_url_format_relative_url_with_scheme_required() -> None:
    """
    Test case 14: Relative URL fails when scheme required.
    """
    # Arrange
    url = "/path/to/resource"

    # Act
    result = validate_url_format(url, require_scheme=True)

    # Assert
    assert result is False


def test_validate_url_format_relative_url_scheme_not_required() -> None:
    """
    Test case 15: Relative URL passes when scheme not required.
    """
    # Arrange
    url = "/path/to/resource"

    # Act
    result = validate_url_format(url, require_scheme=False, require_netloc=False)

    # Assert
    assert result is True


def test_validate_url_format_allowed_schemes() -> None:
    """
    Test case 16: URL scheme must be in allowed list.
    """
    # Arrange
    url = "ftp://example.com/file"
    allowed_schemes = ["http", "https"]

    # Act
    result = validate_url_format(url, allowed_schemes=allowed_schemes)

    # Assert
    assert result is False


def test_validate_url_format_allowed_schemes_match() -> None:
    """
    Test case 17: URL scheme in allowed list.
    """
    # Arrange
    url = "https://example.com"
    allowed_schemes = ["http", "https"]

    # Act
    result = validate_url_format(url, allowed_schemes=allowed_schemes)

    # Assert
    assert result is True


def test_validate_url_format_empty_url() -> None:
    """
    Test case 18: Empty URL is invalid.
    """
    # Arrange
    url = ""

    # Act
    result = validate_url_format(url)

    # Assert
    assert result is False


def test_validate_url_format_invalid_type_raises_error() -> None:
    """
    Test case 19: TypeError for non-string URL.
    """
    # Arrange
    url = 123
    expected_message = "url must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        validate_url_format(url)  # type: ignore


def test_validate_url_format_invalid_port() -> None:
    """
    Test case 20: Invalid port number.
    """
    # Arrange
    url = "http://example.com:99999/path"

    # Act
    result = validate_url_format(url)

    # Assert
    assert result is False
