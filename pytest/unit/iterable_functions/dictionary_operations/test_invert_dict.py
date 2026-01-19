from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.dictionary_operations.invert_dict import invert_dict


def test_invert_dict_basic_inversion() -> None:
    """
    Test case 1: Normal operation with basic dictionary inversion.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2, "c": 3}
    expected_output: dict[Any, str] = {1: "a", 2: "b", 3: "c"}

    # Act
    result = invert_dict(input_data)

    # Assert
    assert result == expected_output


def test_invert_dict_allow_duplicates() -> None:
    """
    Test case 2: Normal operation with duplicate values allowed.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2, "c": 1}
    expected_output: dict[Any, list[str]] = {1: ["a", "c"], 2: ["b"]}

    # Act
    result = invert_dict(input_data, allow_duplicates=True)

    # Assert
    assert result == expected_output


def test_invert_dict_empty_dictionary() -> None:
    """
    Test case 3: Edge case with empty dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {}
    expected_output: dict[Any, str] = {}

    # Act
    result = invert_dict(input_data)

    # Assert
    assert result == expected_output


def test_invert_dict_mixed_value_types() -> None:
    """
    Test case 4: Normal operation with mixed value types.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": "hello", "c": (1, 2)}
    expected_output: dict[Any, str] = {1: "a", "hello": "b", (1, 2): "c"}

    # Act
    result = invert_dict(input_data)

    # Assert
    assert result == expected_output


def test_invert_dict_multiple_duplicates() -> None:
    """
    Test case 5: Normal operation with multiple duplicates.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 1, "c": 2, "d": 1}
    expected_output: dict[Any, list[str]] = {1: ["a", "b", "d"], 2: ["c"]}

    # Act
    result = invert_dict(input_data, allow_duplicates=True)

    # Assert
    assert result == expected_output


def test_invert_dict_single_item() -> None:
    """
    Test case 6: Edge case with single item dictionary.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1}
    expected_output: dict[Any, str] = {1: "a"}

    # Act
    result = invert_dict(input_data)

    # Assert
    assert result == expected_output


def test_invert_dict_no_modification_original() -> None:
    """
    Test case 7: Verify original dictionary is not modified.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    original_data: dict[str, Any] = input_data.copy()

    # Act
    invert_dict(input_data)

    # Assert
    assert input_data == original_data


def test_invert_dict_no_duplicates_with_allow_true() -> None:
    """
    Test case 8: Normal operation with no duplicates but allow_duplicates=True.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 2}
    expected_output: dict[Any, list[str]] = {1: ["a"], 2: ["b"]}

    # Act
    result = invert_dict(input_data, allow_duplicates=True)

    # Assert
    assert result == expected_output


def test_invert_dict_duplicates_not_allowed_error() -> None:
    """
    Test case 9: ValueError for duplicate values when not allowed.
    """
    # Arrange
    input_data: dict[str, Any] = {"a": 1, "b": 1}
    expected_message: str = "Duplicate values found: \\[1\\]"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        invert_dict(input_data, allow_duplicates=False)


def test_invert_dict_invalid_type_error() -> None:
    """
    Test case 10: TypeError for invalid input type.
    """
    # Arrange
    invalid_input: str = "not a dict"
    expected_message: str = "d must be a dictionary, got str"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        invert_dict(invalid_input)
