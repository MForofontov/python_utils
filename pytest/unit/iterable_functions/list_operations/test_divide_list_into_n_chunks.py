import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from pyutils_collection.iterable_functions.list_operations.divide_list_into_n_chunks import (
    divide_list_into_n_chunks,
)


def test_divide_list_into_n_chunks_success() -> None:
    """
    Test case 1: Test the divide_list_into_n_chunks function with valid inputs.
    """
    list_to_divide: list[int] = [1, 2, 3, 4, 5]
    n: int = 2
    expected_output: list[list[int]] = [[1, 2, 3], [4, 5]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output


def test_divide_list_into_n_chunks_exact_division() -> None:
    """
    Test case 2: Test the divide_list_into_n_chunks function with exact division.
    """
    list_to_divide: list[int] = [1, 2, 3, 4]
    n: int = 2
    expected_output: list[list[int]] = [[1, 2], [3, 4]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output


def test_divide_list_into_n_chunks_more_chunks_than_elements() -> None:
    """
    Test case 3: Test the divide_list_into_n_chunks function with more chunks than elements.
    """
    list_to_divide: list[int] = [1, 2]
    n: int = 3
    expected_output: list[list[int]] = [[1], [2], []]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output


def test_divide_list_into_n_chunks_empty_list() -> None:
    """
    Test case 4: Test the divide_list_into_n_chunks function with an empty list.
    """
    list_to_divide: list[int] = []
    n: int = 3
    expected_output: list[list[int]] = [[], [], []]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output


def test_divide_list_into_n_chunks_single_element() -> None:
    """
    Test case 5: Test the divide_list_into_n_chunks function with a single element.
    """
    list_to_divide: list[int] = [1]
    n: int = 1
    expected_output: list[list[int]] = [[1]]
    assert divide_list_into_n_chunks(list_to_divide, n) == expected_output


def test_divide_list_into_n_chunks_type_error_list() -> None:
    """
    Test case 6: Test the divide_list_into_n_chunks function with invalid type for list_to_divide.
    """
    with pytest.raises(TypeError):
        divide_list_into_n_chunks("not a list", 2)


def test_divide_list_into_n_chunks_type_error_n() -> None:
    """
    Test case 7: Test the divide_list_into_n_chunks function with invalid type for n.
    """
    with pytest.raises(TypeError):
        divide_list_into_n_chunks([1, 2, 3], "not an integer")


def test_divide_list_into_n_chunks_value_error_n() -> None:
    """
    Test case 8: Test the divide_list_into_n_chunks function with invalid value for n.
    """
    with pytest.raises(ValueError):
        divide_list_into_n_chunks([1, 2, 3], 0)
