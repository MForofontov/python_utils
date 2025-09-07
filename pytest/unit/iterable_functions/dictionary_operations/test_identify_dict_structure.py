import pytest
from typing import Any
from iterable_functions.identify_dict_structure import identify_dict_structure


def test_identify_dict_structure_success() -> None:
    """
    Test case 1: Test the identify_dict_structure function with valid inputs.
    """
    list_of_dicts: list[dict[str, Any]] = [
        {"a": 1, "b": "string"},
        {"b": "another string", "c": [1, 2, 3]},
        {"d": {"nested": "dict", "e": {"nested_again": "value"}}},
    ]
    expected_output: dict[str, None] = {
        "a": None,
        "b": None,
        "c": None,
        "d": None,
        "d.nested": None,
        "d.e": None,
        "d.e.nested_again": None,
    }
    assert identify_dict_structure(list_of_dicts) == expected_output


def test_identify_dict_structure_empty_list() -> None:
    """
    Test case 2: Test the identify_dict_structure function with an empty list.
    """
    list_of_dicts: list[dict[str, Any]] = []
    expected_output: dict[str, None] = {}
    assert identify_dict_structure(list_of_dicts) == expected_output


def test_identify_dict_structure_single_dict() -> None:
    """
    Test case 3: Test the identify_dict_structure function with a single dictionary.
    """
    list_of_dicts: list[dict[str, Any]] = [{"a": 1, "b": "string"}]
    expected_output: dict[str, None] = {"a": None, "b": None}
    assert identify_dict_structure(list_of_dicts) == expected_output


def test_identify_dict_structure_nested_dicts() -> None:
    """
    Test case 4: Test the identify_dict_structure function with nested dictionaries.
    """
    list_of_dicts: list[dict[str, Any]] = [
        {"a": 1, "b": {"nested": "dict"}},
        {"c": {"nested_again": {"deeply_nested": "value"}}},
    ]
    expected_output: dict[str, None] = {
        "a": None,
        "b": None,
        "b.nested": None,
        "c": None,
        "c.nested_again": None,
        "c.nested_again.deeply_nested": None,
    }
    assert identify_dict_structure(list_of_dicts) == expected_output


def test_identify_dict_structure_dict_with_list_of_dicts() -> None:
    """
    Test case 5: Test the identify_dict_structure function with a dict that contains a dict with a list of dicts.
    """
    list_of_dicts: list[dict[str, Any]] = [
        {"a": 1, "b": {"nested": [{"key1": "value1"}, {"key2": "value2"}]}}
    ]
    expected_output: dict[str, None] = {
        "a": None,
        "b": None,
        "b.nested": None,
        "b.nested.key1": None,
        "b.nested.key2": None,
    }
    assert identify_dict_structure(list_of_dicts) == expected_output


def test_identify_dict_structure_type_error_list_of_dicts() -> None:
    """
    Test case 6: Test the identify_dict_structure function with invalid type for list_of_dicts.
    """
    with pytest.raises(TypeError):
        identify_dict_structure("not a list")


def test_identify_dict_structure_type_error_elements() -> None:
    """
    Test case 7: Test the identify_dict_structure function with invalid elements in list_of_dicts.
    """
    with pytest.raises(TypeError):
        identify_dict_structure([{"a": 1}, "not a dict"])
