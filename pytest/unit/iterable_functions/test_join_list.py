import pytest
from iterable_functions.join_list import join_list


def test_join_list_success() -> None:
    """
    Test case 1: Test the join_list function with valid inputs.
    """
    lst: list[str] = ["apple", "banana", "cherry"]
    delimiter: str = ", "
    expected_output: str = "apple, banana, cherry"
    assert join_list(lst, delimiter) == expected_output


def test_join_list_empty_list() -> None:
    """
    Test case 2: Test the join_list function with an empty list.
    """
    lst: list[str] = []
    delimiter: str = ", "
    expected_output: str = ""
    assert join_list(lst, delimiter) == expected_output


def test_join_list_single_element() -> None:
    """
    Test case 3: Test the join_list function with a single element.
    """
    lst: list[str] = ["apple"]
    delimiter: str = ", "
    expected_output: str = "apple"
    assert join_list(lst, delimiter) == expected_output


def test_join_list_type_error_list() -> None:
    """
    Test case 4: Test the join_list function with invalid type for lst.
    """
    with pytest.raises(TypeError):
        join_list("not a list", ", ")


def test_join_list_type_error_elements() -> None:
    """
    Test case 5: Test the join_list function with invalid elements in lst.
    """
    with pytest.raises(TypeError):
        join_list(["apple", 1, "cherry"], ", ")


def test_join_list_type_error_delimiter() -> None:
    """
    Test case 6: Test the join_list function with invalid type for delimiter.
    """
    with pytest.raises(TypeError):
        join_list(["apple", "banana", "cherry"], 123)
