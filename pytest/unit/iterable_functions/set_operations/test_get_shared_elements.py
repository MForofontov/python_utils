from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from python_utils.iterable_functions.set_operations.get_shared_elements import get_shared_elements


def test_get_shared_elements_success() -> None:
    """
    Test case 1: Test the get_shared_elements function with valid inputs.
    """
    dict_: dict[str, list[int]] = {
        "list1": [1, 2, 3],
        "list2": [2, 3, 4],
        "list3": [3, 4, 5],
    }
    expected_output: list[int] = [2, 3, 4]
    assert get_shared_elements(dict_) == expected_output


def test_get_shared_elements_no_shared_elements() -> None:
    """
    Test case 2: Test the get_shared_elements function with no shared elements.
    """
    dict_: dict[str, list[int]] = {"list1": [1, 2], "list2": [3, 4], "list3": [5, 6]}
    expected_output: list[int] = []
    assert get_shared_elements(dict_) == expected_output


def test_get_shared_elements_empty_dict() -> None:
    """
    Test case 3: Test the get_shared_elements function with an empty dictionary.
    """
    dict_: dict[str, list[int]] = {}
    expected_output: list[int] = []
    assert get_shared_elements(dict_) == expected_output


def test_get_shared_elements_empty_lists() -> None:
    """
    Test case 4: Test the get_shared_elements function with empty lists.
    """
    dict_: dict[str, list[int]] = {"list1": [], "list2": [], "list3": []}
    expected_output: list[int] = []
    assert get_shared_elements(dict_) == expected_output


def test_get_shared_elements_strings() -> None:
    """
    Test case 5: Test the get_shared_elements function with lists of strings.
    """
    dict_: dict[str, list[str]] = {
        "list1": ["apple", "banana"],
        "list2": ["banana", "cherry"],
        "list3": ["banana", "date"],
    }
    expected_output: list[str] = ["banana"]
    assert get_shared_elements(dict_) == expected_output


def test_get_shared_elements_mixed_types() -> None:
    """
    Test case 6: Test the get_shared_elements function with lists of mixed types.
    """
    dict_: dict[str, list[Any]] = {
        "list1": [1, "banana"],
        "list2": [3.14, "banana"],
        "list3": [1, "banana"],
    }
    expected_output: list[Any] = [1, "banana"]
    assert get_shared_elements(dict_) == expected_output


def test_get_shared_elements_type_error_dict() -> None:
    """
    Test case 7: Test the get_shared_elements function with invalid type for dict_.
    """
    with pytest.raises(TypeError):
        get_shared_elements("not a dictionary")


def test_get_shared_elements_type_error_elements() -> None:
    """
    Test case 8: Test the get_shared_elements function with invalid elements in dict_.
    """
    with pytest.raises(TypeError):
        get_shared_elements({"list1": [1, 2], "list2": "not a list"})


def test_get_shared_elements_unhashable_elements() -> None:
    """
    Test case 9: Test the get_shared_elements function with unhashable elements in sublists.
    """
    with pytest.raises(TypeError, match="unhashable type"):
        get_shared_elements({"list1": [1, 2], "list2": [{3: 4}, 5]})
