import pytest
from iterable_functions.divide_list_into_n_chunks import divide_list_into_n_chunks

def test_divide_list_into_n_chunks_success() -> None:
    """
    Test the divide_list_into_n_chunks function with valid inputs.
    """
    # Test case 1: Valid inputs
    list_to_divide: list[int] = [1, 2, 3, 4, 5]
    n: int = 2
    expected_output: list[list[int]] = [[1, 2, 3], [4, 5]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output

def test_divide_list_into_n_chunks_exact_division() -> None:
    """
    Test the divide_list_into_n_chunks function with exact division.
    """
    # Test case 2: Exact division
    list_to_divide: list[int] = [1, 2, 3, 4]
    n: int = 2
    expected_output: list[list[int]] = [[1, 2], [3, 4]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output

def test_divide_list_into_n_chunks_more_chunks_than_elements() -> None:
    """
    Test the divide_list_into_n_chunks function with more chunks than elements.
    """
    # Test case 3: More chunks than elements
    list_to_divide: list[int] = [1, 2]
    n: int = 3
    expected_output: list[list[int]] = [[1], [2]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output

def test_divide_list_into_n_chunks_empty_list() -> None:
    """
    Test the divide_list_into_n_chunks function with an empty list.
    """
    # Test case 4: Empty list
    list_to_divide: list[int] = []
    n: int = 3
    expected_output: list[list[int]] = []
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output

def test_divide_list_into_n_chunks_single_element() -> None:
    """
    Test the divide_list_into_n_chunks function with a single element.
    """
    # Test case 5: Single element
    list_to_divide: list[int] = [1]
    n: int = 1
    expected_output: list[list[int]] = [[1]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output

def test_divide_list_into_n_chunks_type_error_list() -> None:
    """
    Test the divide_list_into_n_chunks function with invalid type for list_to_divide.
    """
    # Test case 6: Invalid type for list_to_divide
    with pytest.raises(TypeError):
        divide_list_into_n_chunks("not a list", 2)

def test_divide_list_into_n_chunks_type_error_n() -> None:
    """
    Test the divide_list_into_n_chunks function with invalid type for n.
    """
    # Test case 7: Invalid type for n
    with pytest.raises(TypeError):
        divide_list_into_n_chunks([1, 2, 3], "not an integer")

def test_divide_list_into_n_chunks_value_error_n() -> None:
    """
    Test the divide_list_into_n_chunks function with invalid value for n.
    """
    # Test case 8: Invalid value for n
    with pytest.raises(ValueError):
        divide_list_into_n_chunks([1, 2, 3], 0)

