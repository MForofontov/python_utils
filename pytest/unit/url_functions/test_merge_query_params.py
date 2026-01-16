"""
Tests for merge_query_params function.
"""

import pytest
from url_functions.merge_query_params import merge_query_params


def test_merge_query_params_add_to_empty() -> None:
    """
    Test case 1: Add parameters to URL without query string.
    """
    # Arrange
    base_url = "http://example.com/path"
    params = {"a": "1", "b": "2"}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "a=1" in result
    assert "b=2" in result
    assert result.startswith("http://example.com/path?")


def test_merge_query_params_merge_existing() -> None:
    """
    Test case 2: Merge with existing query parameters.
    """
    # Arrange
    base_url = "http://example.com?a=1"
    params = {"b": "2"}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "a=1" in result
    assert "b=2" in result


def test_merge_query_params_replace_mode() -> None:
    """
    Test case 3: Replace existing parameters with replace=True.
    """
    # Arrange
    base_url = "http://example.com?a=1&b=2"
    params = {"c": "3"}
    expected = "http://example.com?c=3"

    # Act
    result = merge_query_params(base_url, params, replace=True)

    # Assert
    assert result == expected


def test_merge_query_params_list_values() -> None:
    """
    Test case 4: Handle list values as multiple parameters.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"tags": ["python", "web", "api"]}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "tags=python" in result
    assert "tags=web" in result
    assert "tags=api" in result


def test_merge_query_params_list_with_separator() -> None:
    """
    Test case 5: Handle list values with separator.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"tags": ["python", "web"]}

    # Act
    result = merge_query_params(base_url, params, list_separator=",")

    # Assert
    assert "tags=python%2Cweb" in result


def test_merge_query_params_nested_dict() -> None:
    """
    Test case 6: Handle nested dictionary values.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"filter": {"status": "active", "type": "user"}}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "filter%5Bstatus%5D=active" in result
    assert "filter%5Btype%5D=user" in result


def test_merge_query_params_none_values_skipped() -> None:
    """
    Test case 7: Skip None values.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"a": "1", "b": None, "c": "3"}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "a=1" in result
    assert "c=3" in result
    assert "b=" not in result


def test_merge_query_params_integer_values() -> None:
    """
    Test case 8: Convert integer values to strings.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"page": 2, "limit": 10}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "page=2" in result
    assert "limit=10" in result


def test_merge_query_params_override_existing() -> None:
    """
    Test case 9: Override existing parameter value.
    """
    # Arrange
    base_url = "http://example.com?page=1"
    params = {"page": "2"}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "page=2" in result
    assert "page=1" not in result


def test_merge_query_params_preserve_fragment() -> None:
    """
    Test case 10: Preserve URL fragment.
    """
    # Arrange
    base_url = "http://example.com/path#section"
    params = {"a": "1"}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "#section" in result
    assert "a=1" in result


def test_merge_query_params_empty_url_raises_error() -> None:
    """
    Test case 11: ValueError for empty base_url.
    """
    # Arrange
    base_url = ""
    params = {"a": "1"}
    expected_message = "base_url cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        merge_query_params(base_url, params)


def test_merge_query_params_invalid_url_type_raises_error() -> None:
    """
    Test case 12: TypeError for non-string URL.
    """
    # Arrange
    base_url = 123
    params = {"a": "1"}
    expected_message = "base_url must be a string, got int"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        merge_query_params(base_url, params)  # type: ignore


def test_merge_query_params_invalid_params_type_raises_error() -> None:
    """
    Test case 13: TypeError for non-dict params.
    """
    # Arrange
    base_url = "http://example.com"
    params = "invalid"
    expected_message = "params must be a dict, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        merge_query_params(base_url, params)  # type: ignore


def test_merge_query_params_empty_list() -> None:
    """
    Test case 14: Handle empty list values.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"tags": []}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    # Empty list should not add any parameters
    assert "tags=" not in result


def test_merge_query_params_boolean_values() -> None:
    """
    Test case 15: Convert boolean values to strings.
    """
    # Arrange
    base_url = "http://example.com"
    params = {"active": True, "verified": False}

    # Act
    result = merge_query_params(base_url, params)

    # Assert
    assert "active=True" in result
    assert "verified=False" in result
