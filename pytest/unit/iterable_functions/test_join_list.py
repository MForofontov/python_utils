import pytest
from iterable_functions.join_list import join_list


def test_join_list_success() -> None:
    """
    Test the join_list function with valid inputs.
    """
    # Test case 1: Valid inputs
    lst: list[str] = ["apple", "banana", "cherry"]
    delimiter: str = ", "
    expected_output: str = "apple, banana, cherry"
    assert join_list(lst, delimiter) == expected_output


def test_join_list_empty_list() -> None:
    """
    Test the join_list function with an empty list.
    """
    # Test case 2: Empty list
    lst: list[str] = []
    delimiter: str = ", "
    expected_output: str = ""
    assert join_list(lst, delimiter) == expected_output


def test_join_list_single_element() -> None:
    """
    Test the join_list function with a single element.
    """
    # Test case 3: Single element
    lst: list[str] = ["apple"]
    delimiter: str = ", "
    expected_output: str = "apple"
    assert join_list(lst, delimiter) == expected_output


def test_join_list_type_error_list() -> None:
    """
    Test the join_list function with invalid type for lst.
    """
    # Test case 4: Invalid type for lst
    with pytest.raises(TypeError):
        join_list("not a list", ", ")


def test_join_list_type_error_elements() -> None:
    """
    Test the join_list function with invalid elements in lst.
    """
    # Test case 5: Invalid elements in lst
    with pytest.raises(TypeError):
        join_list(["apple", 1, "cherry"], ", ")


def test_join_list_type_error_delimiter() -> None:
    """
    Test the join_list function with invalid type for delimiter.
    """
    # Test case 6: Invalid type for delimiter
    with pytest.raises(TypeError):
        join_list(["apple", "banana", "cherry"], 123)
