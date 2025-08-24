import pytest
from iterable_functions.get_max_min_values import get_max_min_values


def test_get_max_min_values_list() -> None:
    """
    Test case 1: Test the get_max_min_values function with a list of integers.
    """
    input_collection: list[int | float] = [1, 2, 3, 4, 5]
    expected_output: tuple[int | float, int | float] = (5, 1)
    assert get_max_min_values(input_collection) == expected_output


def test_get_max_min_values_set() -> None:
    """
    Test case 2: Test the get_max_min_values function with a set of integers.
    """
    input_collection: set[int | float] = {1, 2, 3, 4, 5}
    expected_output: tuple[int | float, int | float] = (5, 1)
    assert get_max_min_values(input_collection) == expected_output


def test_get_max_min_values_tuple() -> None:
    """
    Test case 3: Test the get_max_min_values function with a tuple of integers.
    """
    input_collection: tuple[int | float, ...] = (1, 2, 3, 4, 5)
    expected_output: tuple[int | float, int | float] = (5, 1)
    assert get_max_min_values(input_collection) == expected_output


def test_get_max_min_values_floats() -> None:
    """
    Test case 4: Test the get_max_min_values function with a collection of floats.
    """
    input_collection: list[float] = [1.1, 2.2, 3.3, 4.4, 5.5]
    expected_output: tuple[float, float] = (5.5, 1.1)
    assert get_max_min_values(input_collection) == expected_output


def test_get_max_min_values_mixed_types() -> None:
    """
    Test case 5: Test the get_max_min_values function with a collection of mixed types.
    """
    input_collection: list[int | float] = [1, 2.2, 3, 4.4, 5]
    expected_output: tuple[int | float, int | float] = (5, 1)
    assert get_max_min_values(input_collection) == expected_output


def test_get_max_min_values_single_element() -> None:
    """
    Test case 6: Test the get_max_min_values function with a single element.
    """
    input_collection: list[int] = [1]
    expected_output: tuple[int, int] = (1, 1)
    assert get_max_min_values(input_collection) == expected_output


def test_get_max_min_values_empty_collection() -> None:
    """
    Test case 7: Test the get_max_min_values function with an empty collection.
    """
    input_collection: list[int] = []
    with pytest.raises(ValueError):
        get_max_min_values(input_collection)


def test_get_max_min_values_type_error_collection() -> None:
    """
    Test case 8: Test the get_max_min_values function with invalid type for input_collection.
    """
    with pytest.raises(TypeError):
        get_max_min_values("not a list, set, or tuple")


def test_get_max_min_values_type_error_elements() -> None:
    """
    Test case 9: Test the get_max_min_values function with invalid elements in input_collection.
    """
    with pytest.raises(TypeError):
        get_max_min_values([1, 2, "three", 4, 5])
