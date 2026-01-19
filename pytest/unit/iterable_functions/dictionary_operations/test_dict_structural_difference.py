from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.dictionary_operations.dict_structural_difference import (
    dict_structural_difference,
)


def test_dict_structural_difference_identical_dicts() -> None:
    """
    Test case 1: Normal operation with identical dictionaries.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": 1, "b": 2}
    dict2: dict[str, Any] = {"a": 1, "b": 2}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": [],
        "unchanged": ["a", "b"],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_added_keys() -> None:
    """
    Test case 2: Normal operation with added keys.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": 1}
    dict2: dict[str, Any] = {"a": 1, "b": 2}
    expected_output: dict[str, list[str]] = {
        "added": ["b"],
        "removed": [],
        "modified": [],
        "unchanged": ["a"],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_removed_keys() -> None:
    """
    Test case 3: Normal operation with removed keys.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": 1, "b": 2}
    dict2: dict[str, Any] = {"a": 1}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": ["b"],
        "modified": [],
        "unchanged": ["a"],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_modified_values() -> None:
    """
    Test case 4: Normal operation with modified values.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": 1, "b": 2}
    dict2: dict[str, Any] = {"a": 1, "b": 3}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": ["b"],
        "unchanged": ["a"],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_mixed_changes() -> None:
    """
    Test case 5: Normal operation with mixed changes.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": 1, "b": 2, "c": 3}
    dict2: dict[str, Any] = {"a": 1, "b": 4, "d": 5}
    expected_output: dict[str, list[str]] = {
        "added": ["d"],
        "removed": ["c"],
        "modified": ["b"],
        "unchanged": ["a"],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_nested_dictionaries() -> None:
    """
    Test case 6: Normal operation with nested dictionaries.
    """
    # Arrange
    dict1: dict[str, Any] = {"user": {"name": "John", "age": 30}}
    dict2: dict[str, Any] = {"user": {"name": "John", "age": 31}}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": ["user"],
        "unchanged": [],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_nested_recursive_comparison() -> None:
    """
    Test case 7: Normal operation with nested dictionaries using recursive comparison.
    """
    # Arrange
    dict1: dict[str, Any] = {"user": {"name": "John", "age": 30}}
    dict2: dict[str, Any] = {"user": {"name": "John", "age": 31}}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": ["user"],
        "unchanged": [],
    }

    # Act
    result = dict_structural_difference(dict1, dict2, recursive=True)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_empty_dicts() -> None:
    """
    Test case 8: Edge case with empty dictionaries.
    """
    # Arrange
    dict1: dict[str, Any] = {}
    dict2: dict[str, Any] = {}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": [],
        "unchanged": [],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_one_empty_dict() -> None:
    """
    Test case 9: Edge case with one empty dictionary.
    """
    # Arrange
    dict1: dict[str, Any] = {}
    dict2: dict[str, Any] = {"a": 1}
    expected_output: dict[str, list[str]] = {
        "added": ["a"],
        "removed": [],
        "modified": [],
        "unchanged": [],
    }

    # Act
    result = dict_structural_difference(dict1, dict2)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_complex_nested_structure() -> None:
    """
    Test case 10: Normal operation with complex nested structure.
    """
    # Arrange
    dict1: dict[str, Any] = {
        "users": {
            "john": {"age": 30, "active": True},
            "jane": {"age": 25, "active": False},
        }
    }
    dict2: dict[str, Any] = {
        "users": {
            "john": {"age": 31, "active": True},
            "bob": {"age": 35, "active": True},
        }
    }
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": ["users"],
        "unchanged": [],
    }

    # Act
    result = dict_structural_difference(dict1, dict2, recursive=True)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_no_changes_deeply_nested() -> None:
    """
    Test case 11: Edge case with no changes in deeply nested structure.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": {"b": {"c": 1}}}
    dict2: dict[str, Any] = {"a": {"b": {"c": 1}}}
    expected_output: dict[str, list[str]] = {
        "added": [],
        "removed": [],
        "modified": [],
        "unchanged": ["a"],
    }

    # Act
    result = dict_structural_difference(dict1, dict2, recursive=True)

    # Assert
    assert result == expected_output


def test_dict_structural_difference_type_error_invalid_input() -> None:
    """
    Test case 12: TypeError for invalid input types.
    """
    # Arrange
    dict1: dict[str, Any] = {"a": 1}
    invalid_dict2: str = "not a dict"
    expected_message: str = "Both dict1 and dict2 must be dictionaries"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        dict_structural_difference(dict1, invalid_dict2)
