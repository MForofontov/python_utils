import pytest
from typing import Any
from iterable_functions.identify_value_in_dict_get_key import (
    identify_value_in_dict_get_key,
)


def test_identify_value_in_dict_get_key_success() -> None:
    """
    Test the identify_value_in_dict_get_key function with valid inputs.
    """
    # Test case 1: Valid inputs
    dictionary: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    target_value: int = 2
    expected_output: str = "b"
    assert identify_value_in_dict_get_key(
        target_value, dictionary) == expected_output


def test_identify_value_in_dict_get_key_not_found() -> None:
    """
    Test the identify_value_in_dict_get_key function with a value not found.
    """
    # Test case 2: Value not found
    dictionary: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    target_value: int = 4
    expected_output: None = None
    assert identify_value_in_dict_get_key(
        target_value, dictionary) == expected_output


def test_identify_value_in_dict_get_key_empty_dict() -> None:
    """
    Test the identify_value_in_dict_get_key function with an empty dictionary.
    """
    # Test case 3: Empty dictionary
    dictionary: dict[str, int] = {}
    target_value: int = 1
    expected_output: None = None
    assert identify_value_in_dict_get_key(
        target_value, dictionary) == expected_output


def test_identify_value_in_dict_get_key_strings() -> None:
    """
    Test the identify_value_in_dict_get_key function with strings.
    """
    # Test case 4: Strings
    dictionary: dict[str, str] = {"a": "apple", "b": "banana", "c": "cherry"}
    target_value: str = "banana"
    expected_output: str = "b"
    assert identify_value_in_dict_get_key(
        target_value, dictionary) == expected_output


def test_identify_value_in_dict_get_key_mixed_types() -> None:
    """
    Test the identify_value_in_dict_get_key function with mixed types.
    """
    # Test case 5: Mixed types
    dictionary: dict[str | int, Any] = {"a": 1, 2: "banana", "c": 3.14}
    target_value: Any = "banana"
    expected_output: str | int = 2
    assert identify_value_in_dict_get_key(
        target_value, dictionary) == expected_output


def test_identify_value_in_dict_get_key_type_error_dict() -> None:
    """
    Test the identify_value_in_dict_get_key function with invalid type for dictionary.
    """
    # Test case 6: Invalid type for dictionary
    with pytest.raises(TypeError):
        identify_value_in_dict_get_key(1, "not a dictionary")
