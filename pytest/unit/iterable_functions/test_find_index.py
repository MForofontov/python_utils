import pytest
from iterable_functions.find_index import find_index


def test_find_index_success() -> None:
    """
    Test the find_index function with valid inputs where the target string is found.
    """
    # Test case 1: Target string is found
    input_list: list[str] = ["apple", "banana", "cherry"]
    target_string: str = "banana"
    expected_output: int = 1
    assert find_index(input_list, target_string) == expected_output


def test_find_index_not_found() -> None:
    """
    Test the find_index function with valid inputs where the target string is not found.
    """
    # Test case 2: Target string is not found
    input_list: list[str] = ["apple", "banana", "cherry"]
    target_string: str = "date"
    expected_output: None = None
    assert find_index(input_list, target_string) == expected_output


def test_find_index_empty_list() -> None:
    """
    Test the find_index function with an empty list.
    """
    # Test case 3: Empty list
    input_list: list[str] = []
    target_string: str = "apple"
    expected_output: None = None
    assert find_index(input_list, target_string) == expected_output


def test_find_index_multiple_occurrences() -> None:
    """
    Test the find_index function with multiple occurrences of the target string.
    """
    # Test case 4: Multiple occurrences of the target string
    input_list: list[str] = ["apple", "banana", "apple", "cherry"]
    target_string: str = "apple"
    expected_output: int = 0
    assert find_index(input_list, target_string) == expected_output


def test_find_index_type_error_input_list() -> None:
    """
    Test the find_index function with invalid type for input_list.
    """
    # Test case 5: Invalid type for input_list
    with pytest.raises(TypeError):
        find_index("not a list", "apple")


def test_find_index_type_error_elements() -> None:
    """
    Test the find_index function with invalid elements in input_list.
    """
    # Test case 6: Invalid elements in input_list
    with pytest.raises(TypeError):
        find_index(["apple", 1, "cherry"], "apple")


def test_find_index_type_error_target_string() -> None:
    """
    Test the find_index function with invalid type for target_string.
    """
    # Test case 7: Invalid type for target_string
    with pytest.raises(TypeError):
        find_index(["apple", "banana", "cherry"], 123)
