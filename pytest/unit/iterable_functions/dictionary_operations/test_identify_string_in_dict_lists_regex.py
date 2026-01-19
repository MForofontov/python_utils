import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from iterable_functions.dictionary_operations.identify_string_in_dict_lists_regex import (
    identify_string_in_dict_lists_regex,
)


def test_identify_string_in_dict_lists_regex_success() -> None:
    """
    Test case 1: Test the identify_string_in_dict_lists_regex function with valid inputs.
    """
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
    Test case 2: Test the identify_string_in_dict_lists_regex function with a value not found.
    """
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
    Test case 3: Test the identify_string_in_dict_lists_regex function with an empty dictionary.
    """
    dict_of_lists: dict[str | int, list[list[str]]] = {}
    target_value: str = "apple"
    expected_output = None
    assert (
        identify_string_in_dict_lists_regex(target_value, dict_of_lists)
        == expected_output
    )


def test_identify_string_in_dict_lists_regex_regex() -> None:
    """
    Test case 4: Test the identify_string_in_dict_lists_regex function with regex enabled.
    """
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
    Test case 5: Test the identify_string_in_dict_lists_regex function with invalid type for target_value.
    """
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            123, {"key1": [["apple", "banana"]]}, regex=None
        )


def test_identify_string_in_dict_lists_regex_type_error_dict_of_lists() -> None:
    """
    Test case 6: Test the identify_string_in_dict_lists_regex function with invalid type for dict_of_lists.
    """
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex("apple", "not a dictionary", regex=None)


def test_identify_string_in_dict_lists_regex_type_error_elements() -> None:
    """
    Test case 7: Test the identify_string_in_dict_lists_regex function with invalid elements in dict_of_lists.
    """
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            "apple", {"key1": ["not a list"]}, regex=None
        )


def test_identify_string_in_dict_lists_regex_type_error_regex() -> None:
    """
    Test case 8: Test the identify_string_in_dict_lists_regex function with invalid type for regex.
    """
    with pytest.raises(TypeError):
        identify_string_in_dict_lists_regex(
            "apple", {"key1": [["apple", "banana"]]}, regex=123
        )
