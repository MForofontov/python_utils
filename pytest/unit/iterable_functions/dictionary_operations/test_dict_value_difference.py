"""Unit tests for dict_value_difference function."""
import pytest

from iterable_functions.dictionary_operations.dict_value_difference import (
    dict_value_difference,
)


def test_dict_value_difference_basic_difference() -> None:
    """
    Test case 1: Basic dictionary value differences.
    """
    # Arrange
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 5, "d": 4}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {"b": 5, "d": 4, "c": None}


def test_dict_value_difference_ignore_missing() -> None:
    """
    Test case 2: Ignore missing keys with ignore_missing=True.
    """
    # Arrange
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 5, "d": 4}

    # Act
    result = dict_value_difference(dict1, dict2, ignore_missing=True)

    # Assert
    assert result == {"b": 5}


def test_dict_value_difference_no_differences() -> None:
    """
    Test case 3: Identical dictionaries return empty dict.
    """
    # Arrange
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"a": 1, "b": 2, "c": 3}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {}


def test_dict_value_difference_empty_dicts() -> None:
    """
    Test case 4: Both empty dictionaries.
    """
    # Arrange
    dict1: dict[str, int] = {}
    dict2: dict[str, int] = {}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {}


def test_dict_value_difference_one_empty() -> None:
    """
    Test case 5: One dictionary is empty.
    """
    # Arrange
    dict1 = {"a": 1, "b": 2}
    dict2: dict[str, int] = {}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {"a": None, "b": None}


def test_dict_value_difference_new_keys_only() -> None:
    """
    Test case 6: All keys in dict2 are new.
    """
    # Arrange
    dict1 = {"a": 1}
    dict2 = {"b": 2, "c": 3}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {"b": 2, "c": 3, "a": None}


def test_dict_value_difference_nested_values() -> None:
    """
    Test case 7: Dictionaries with nested values (shallow comparison).
    """
    # Arrange
    dict1 = {"a": [1, 2], "b": {"x": 1}}
    dict2 = {"a": [1, 2], "b": {"x": 2}}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {"b": {"x": 2}}


def test_dict_value_difference_different_value_types() -> None:
    """
    Test case 8: Values change types between dictionaries.
    """
    # Arrange
    dict1 = {"a": 1, "b": "text", "c": True}
    dict2 = {"a": "1", "b": 2, "c": False}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {"a": "1", "b": 2, "c": False}


def test_dict_value_difference_none_values() -> None:
    """
    Test case 9: Dictionaries with None values.
    """
    # Arrange
    dict1 = {"a": 1, "b": None}
    dict2 = {"a": None, "b": None}

    # Act
    result = dict_value_difference(dict1, dict2)

    # Assert
    assert result == {"a": None}
def test_dict_value_difference_type_error_non_dict_dict1() -> None:
    """
    Test case 10: TypeError when dict1 is not a dictionary.
    """
    # Arrange
    invalid_dict1 = "not a dict"
    dict2 = {"a": 1}

    # Act & Assert
    with pytest.raises(TypeError, match="dict1 must be a dictionary"):
        dict_value_difference(invalid_dict1, dict2)  # type: ignore


def test_dict_value_difference_type_error_non_dict_dict2() -> None:
    """
    Test case 11: TypeError when dict2 is not a dictionary.
    """
    # Arrange
    dict1 = {"a": 1}
    invalid_dict2 = [1, 2, 3]

    # Act & Assert
    with pytest.raises(TypeError, match="dict2 must be a dictionary"):
        dict_value_difference(dict1, invalid_dict2)  # type: ignore


def test_dict_value_difference_type_error_non_bool_ignore_missing() -> None:
    """
    Test case 12: TypeError when ignore_missing is not a boolean.
    """
    # Arrange
    dict1 = {"a": 1}
    dict2 = {"b": 2}
    invalid_ignore = "yes"

    # Act & Assert
    with pytest.raises(TypeError, match="ignore_missing must be a boolean"):
        dict_value_difference(dict1, dict2, ignore_missing=invalid_ignore)  # type: ignore
