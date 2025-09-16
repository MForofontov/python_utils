from typing import Any

import pytest
from iterable_functions.dictionary_operations.flatten_dict import flatten_dict


def test_flatten_dict_case_1_basic_flat_dictionary() -> None:
    """
    Test case 1: Basic operation with flat dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2, "c": 3}
    expected_output: dict[str, Any] = {"a": 1, "b": 2, "c": 3}

    # Act
    result = flatten_dict(input_data)

    # Assert
    assert result == expected_output


def test_flatten_dict_case_2_nested_dictionary() -> None:
    """
    Test case 2: Normal operation with nested dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": {"c": 2, "d": 3}}
    expected_output: dict[str, Any] = {"a": 1, "b_c": 2, "b_d": 3}

    # Act
    result = flatten_dict(input_data)

    # Assert
    assert result == expected_output


def test_flatten_dict_case_3_deeply_nested_dictionary() -> None:
    """
    Test case 3: Normal operation with deeply nested dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": {"b": {"c": {"d": 1}}}}
    expected_output: dict[str, Any] = {"a_b_c_d": 1}

    # Act
    result = flatten_dict(input_data)

    # Assert
    assert result == expected_output


def test_flatten_dict_case_4_custom_separator() -> None:
    """
    Test case 4: Normal operation with custom separator.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": {"b": 1, "c": 2}}
    expected_output: dict[str, Any] = {"a.b": 1, "a.c": 2}

    # Act
    result = flatten_dict(input_data, separator=".")

    # Assert
    assert result == expected_output


def test_flatten_dict_case_5_with_prefix() -> None:
    """
    Test case 5: Normal operation with prefix.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    expected_output: dict[str, Any] = {"root_a": 1, "root_b": 2}

    # Act
    result = flatten_dict(input_data, prefix="root")

    # Assert
    assert result == expected_output


def test_flatten_dict_case_6_mixed_value_types() -> None:
    """
    Test case 6: Normal operation with mixed value types.
    """
    # Arrange
    input_data: dict[str, Any] = {
        "string": "hello",
        "number": 42,
        "list": [1, 2, 3],
        "nested": {"key": "value"},
    }
    expected_output: dict[str, Any] = {
        "string": "hello",
        "number": 42,
        "list": [1, 2, 3],
        "nested_key": "value",
    }

    # Act
    result = flatten_dict(input_data)

    # Assert
    assert result == expected_output


def test_flatten_dict_case_7_empty_dictionary() -> None:
    """
    Test case 7: Edge case with empty dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    expected_output: dict[str, Any] = {}

    # Act
    result = flatten_dict(input_data)

    # Assert
    assert result == expected_output


def test_flatten_dict_case_8_invalid_type_error() -> None:
    """
    Test case 8: TypeError for invalid input type.
    """
    # Arrange
    invalid_input: str = "not a dict"
    expected_message: str = "d must be a dictionary, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        flatten_dict(invalid_input)


def test_flatten_dict_case_9_no_modification_original() -> None:
    """
    Test case 9: Verify original dictionary is not modified.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": {"b": 1}}
    original_data: dict[str, Any] = input_data.copy()

    # Act
    flatten_dict(input_data)

    # Assert
    assert input_data == original_data


def test_flatten_dict_case_10_complex_separator() -> None:
    """
    Test case 10: Normal operation with complex separator.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": {"b": {"c": 1}}}
    expected_output: dict[str, Any] = {"a__b__c": 1}

    # Act
    result = flatten_dict(input_data, separator="__")

    # Assert
    assert result == expected_output
