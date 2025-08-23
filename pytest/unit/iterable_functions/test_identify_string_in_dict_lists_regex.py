import pytest
from iterable_functions.identify_string_in_dict_lists_regex import (
    identify_string_in_dict_lists_regex,
)


def test_identify_string_in_dict_lists_regex_success() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with valid inputs.
    """
    # Test case 1: Valid inputs
    dict_of_lists: dict[str | int, list[list[str]]] = {
        "key1": [["apple", "banana"], ["cherry", "date"]],
        "key2": [["fig", "grape"], ["apple", "kiwi"]],
    }
    target_value: str = "apple"
    expected_output: str = "key1"
    assert (
        identify_string_in_dict_lists_regex(target_value, dict_of_lists)
        == expected_output
    )


def test_identify_string_in_dict_lists_regex_not_found() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with a value not found.
    """
    # Test case 2: Value not found
    dict_of_lists: dict[str | int, list[list[str]]] = {
        "key1": [["apple", "banana"], ["cherry", "date"]],
        "key2": [["fig", "grape"], ["kiwi", "lemon"]],
    }
    target_value: str = "orange"
    expected_output = None
    assert (
        identify_string_in_dict_lists_regex(target_value, dict_of_lists)
        == expected_output
    )


def test_identify_string_in_dict_lists_regex_empty_dict() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with an empty dictionary.
    """
    # Test case 3: Empty dictionary
    dict_of_lists: dict[str | int, list[list[str]]] = {}
    target_value: str = "apple"
    expected_output = None
    assert (
        identify_string_in_dict_lists_regex(target_value, dict_of_lists)
        == expected_output
    )


def test_identify_string_in_dict_lists_regex_regex() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with regex enabled.
    """
    # Test case 4: Regex enabled
    dict_of_lists: dict[str | int, list[list[str]]] = {
        "key1": [["apple", "banana"], ["cherry", "date"]],
        "key2": [["fig", "grape"], ["apple", "kiwi"]],
    }
    target_value: str = "ap.*"
    expected_output: str = "key1"
    assert (
        identify_string_in_dict_lists_regex(
            target_value, dict_of_lists, regex=target_value
        )
        == expected_output
    )


def test_identify_string_in_dict_lists_regex_type_error_target_value() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with invalid type for target_value.
    """
    # Test case 5: Invalid type for target_value
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            123, {"key1": [["apple", "banana"]]}, regex=None
        )


def test_identify_string_in_dict_lists_regex_type_error_dict_of_lists() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with invalid type for dict_of_lists.
    """
    # Test case 6: Invalid type for dict_of_lists
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            "apple", "not a dictionary", regex=None)


def test_identify_string_in_dict_lists_regex_type_error_elements() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with invalid elements in dict_of_lists.
    """
    # Test case 7: Invalid elements in dict_of_lists
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            "apple", {"key1": ["not a list"]}, regex=None
        )


def test_identify_string_in_dict_lists_regex_type_error_regex() -> None:
    """
    Test the identify_string_in_dict_lists_regex function with invalid type for regex.
    """
    # Test case 8: Invalid type for regex
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            "apple", {"key1": [["apple", "banana"]]}, regex=123
        )
