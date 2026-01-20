from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.dictionary_operations.filter_dict_by_keys import (
    filter_dict_by_keys,
)


def test_filter_dict_by_keys_exact_key_matches() -> None:
    """
    Test case 1: Normal operation with exact key matches.
    """
    # Arrange
    input_data: dict[str, Any] = {
        "name": "John",
        "age": 30,
        "city": "NYC",
        "email": "john@example.com",
    }
    filter_keys: list[str] = ["name", "age"]
    expected_output: dict[str, Any] = {"name": "John", "age": 30}

    # Act
    result = filter_dict_by_keys(input_data, filter_keys)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_set_of_keys() -> None:
    """
    Test case 2: Normal operation with set of keys.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2, "c": 3, "d": 4}
    filter_keys: set[str] = {"a", "c"}
    expected_output: dict[str, Any] = {"a": 1, "c": 3}

    # Act
    result = filter_dict_by_keys(input_data, filter_keys)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_regex_pattern() -> None:
    """
    Test case 3: Normal operation with regex pattern.
    """
    # Arrange
    input_data: dict[str, Any] = {
        "name": "John",
        "age": 30,
        "city": "NYC",
        "email": "john@example.com",
    }
    pattern: str = r"name|email"
    expected_output: dict[str, Any] = {"name": "John", "email": "john@example.com"}

    # Act
    result = filter_dict_by_keys(input_data, pattern=pattern)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_invert_filter() -> None:
    """
    Test case 4: Normal operation with invert flag.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2, "c": 3}
    filter_keys: list[str] = ["a"]
    expected_output: dict[str, Any] = {"b": 2, "c": 3}

    # Act
    result = filter_dict_by_keys(input_data, filter_keys, invert=True)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_pattern_with_invert() -> None:
    """
    Test case 5: Normal operation with pattern and invert.
    """
    # Arrange
    input_data: dict[str, Any] = {"test1": 1, "other": 2, "test2": 3}
    pattern: str = r"^test"
    expected_output: dict[str, Any] = {"other": 2}

    # Act
    result = filter_dict_by_keys(input_data, pattern=pattern, invert=True)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_no_matches() -> None:
    """
    Test case 6: Edge case with no matches.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    filter_keys: list[str] = ["c", "d"]
    expected_output: dict[str, Any] = {}

    # Act
    result = filter_dict_by_keys(input_data, filter_keys)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_empty_keys_list() -> None:
    """
    Test case 7: Edge case with empty keys list.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    filter_keys: list[str] = []
    expected_output: dict[str, Any] = {}

    # Act
    result = filter_dict_by_keys(input_data, filter_keys)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_no_keys_no_pattern() -> None:
    """
    Test case 8: Edge case with no keys and no pattern.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    expected_output: dict[str, Any] = {"a": 1, "b": 2}

    # Act
    result = filter_dict_by_keys(input_data)

    # Assert
    assert result == expected_output


def test_filter_dict_by_keys_no_modification_original() -> None:
    """
    Test case 9: Verify original dictionary is not modified.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2, "c": 3}
    original_data: dict[str, Any] = input_data.copy()
    filter_keys: list[str] = ["a"]

    # Act
    filter_dict_by_keys(input_data, filter_keys)

    # Assert
    assert input_data == original_data


def test_filter_dict_by_keys_invalid_dict_type_error() -> None:
    """
    Test case 10: TypeError for invalid dictionary input.
    """
    # Arrange
    invalid_input: str = "not a dict"
    filter_keys: list[str] = ["a"]
    expected_message: str = "d must be a dictionary, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        filter_dict_by_keys(invalid_input, filter_keys)


def test_filter_dict_by_keys_invalid_keys_type_error() -> None:
    """
    Test case 11: TypeError for invalid keys type.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    invalid_keys: str = "not list or set"
    expected_message: str = "keys must be a list or set, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        filter_dict_by_keys(input_data, invalid_keys)
