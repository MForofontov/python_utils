from typing import Any

import pytest
from iterable_functions.dictionary_operations.deep_get import deep_get


def test_deep_get_basic_functionality() -> None:
    """
    Test case 1: Normal operation with basic deep get functionality.
    """
    # Arrange
    input_data: dict[str, Any] = {"user": {"name": "John", "age": 30}}
    key_path: str = "user.name"
    expected_output: str = "John"

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_list_of_keys() -> None:
    """
    Test case 2: Normal operation with list of keys.
    """
    # Arrange
    input_data: dict[str, Any] = {"user": {"profile": {"settings": {"theme": "dark"}}}}
    key_path: list[str] = ["user", "profile", "settings", "theme"]
    expected_output: str = "dark"

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_default_value() -> None:
    """
    Test case 3: Normal operation with default value for missing key.
    """
    # Arrange
    input_data: dict[str, Any] = {"user": {"name": "John"}}
    key_path: str = "user.email"
    default_value: str = "not found"
    expected_output: str = "not found"

    # Act
    result = deep_get(input_data, key_path, default_value)

    # Assert
    assert result == expected_output


def test_deep_get_missing_key() -> None:
    """
    Test case 4: Edge case with missing key (returns None).
    """
    # Arrange
    input_data: dict[str, Any] = {"user": {"name": "John"}}
    key_path: str = "user.email"
    expected_output: None = None

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_partial_path() -> None:
    """
    Test case 5: Edge case with partial path existing.
    """
    # Arrange
    input_data: dict[str, Any] = {"user": {"name": "John"}}
    key_path: str = "user.profile.age"
    expected_output: None = None

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_empty_dictionary() -> None:
    """
    Test case 6: Edge case with empty dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    key_path: str = "any.key"
    expected_output: None = None

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_root_level_key() -> None:
    """
    Test case 7: Normal operation with root level key.
    """
    # Arrange
    input_data: dict[str, Any] = {"name": "John", "age": 30}
    key_path: str = "name"
    expected_output: str = "John"

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_invalid_type_error() -> None:
    """
    Test case 8: TypeError for invalid input type.
    """
    # Arrange
    invalid_input: str = "not a dict"
    key_path: str = "key"
    expected_message: str = "d must be a dictionary, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        deep_get(invalid_input, key_path)


def test_deep_get_deeply_nested_structure() -> None:
    """
    Test case 9: Normal operation with deeply nested structure.
    """
    # Arrange
    input_data: dict[str, Any] = {"level1": {"level2": {"level3": {"level4": "value"}}}}
    key_path: str = "level1.level2.level3.level4"
    expected_output: str = "value"

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_mixed_data_types() -> None:
    """
    Test case 10: Normal operation with mixed data types.
    """
    # Arrange
    input_data: dict[str, Any] = {
        "users": [
            {"name": "John", "scores": [85, 90]},
            {"name": "Jane", "scores": [95, 88]},
        ]
    }
    key_path: str = "users"
    expected_output: list[dict[str, Any]] = [
        {"name": "John", "scores": [85, 90]},
        {"name": "Jane", "scores": [95, 88]},
    ]

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output


def test_deep_get_empty_string_in_path() -> None:
    """
    Test case 11: Edge case with empty string in path.
    """
    # Arrange
    input_data: dict[str, Any] = {"": {"nested": "value"}}
    key_path: str = ".nested"
    expected_output: str = "value"

    # Act
    result = deep_get(input_data, key_path)

    # Assert
    assert result == expected_output
