import pytest

pytestmark = [pytest.mark.unit, pytest.mark.iterable_functions]
from iterable_functions.set_operations.get_combinations import get_combinations


def test_get_combinations_basic_two_elements() -> None:
    """
    Test case 1: Get combinations of 2 elements from set.
    """
    # Arrange
    input_set = {1, 2, 3, 4}

    # Act
    result = get_combinations(input_set, 2)

    # Assert
    assert result == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]


def test_get_combinations_three_elements() -> None:
    """
    Test case 2: Get combinations of 3 elements.
    """
    # Arrange
    input_set = {1, 2, 3, 4}

    # Act
    result = get_combinations(input_set, 3)

    # Assert
    assert result == [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]


def test_get_combinations_zero_elements() -> None:
    """
    Test case 3: Combinations of 0 elements returns empty list.
    """
    # Arrange
    input_set = {1, 2, 3}

    # Act
    result = get_combinations(input_set, 0)

    # Assert
    assert result == [[]]


def test_get_combinations_full_set() -> None:
    """
    Test case 4: Combinations equal to set size returns single combination.
    """
    # Arrange
    input_set = {1, 2, 3, 4}

    # Act
    result = get_combinations(input_set, 4)

    # Assert
    assert result == [[1, 2, 3, 4]]


def test_get_combinations_single_element() -> None:
    """
    Test case 5: Combinations of 1 element.
    """
    # Arrange
    input_set = {1, 2, 3}

    # Act
    result = get_combinations(input_set, 1)

    # Assert
    assert result == [[1], [2], [3]]


def test_get_combinations_string_set() -> None:
    """
    Test case 6: Combinations from string set.
    """
    # Arrange
    input_set = {"a", "b", "c"}

    # Act
    result = get_combinations(input_set, 2)

    # Assert
    assert len(result) == 3
    assert all(len(comb) == 2 for comb in result)


def test_get_combinations_empty_set() -> None:
    """
    Test case 7: Empty set with r=0 returns empty list in list.
    """
    # Arrange
    input_set: set[int] = set()

    # Act
    result = get_combinations(input_set, 0)

    # Assert
    assert result == [[]]


def test_get_combinations_lexicographic_order() -> None:
    """
    Test case 8: Results are in lexicographic order.
    """
    # Arrange
    input_set = {3, 1, 4, 2}

    # Act
    result = get_combinations(input_set, 2)

    # Assert
    assert result == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    # Verify sorted order
    assert result == sorted(result)


def test_get_combinations_type_error_non_set() -> None:
    """
    Test case 9: TypeError when input_set is not a set.
    """
    # Arrange
    invalid_input = [1, 2, 3]

    # Act & Assert
    with pytest.raises(TypeError, match="input_set must be a set"):
        get_combinations(invalid_input, 2)  # type: ignore


def test_get_combinations_type_error_non_int_r() -> None:
    """
    Test case 10: TypeError when r is not an integer.
    """
    # Arrange
    input_set = {1, 2, 3}

    # Act & Assert
    with pytest.raises(TypeError, match="r must be an int"):
        get_combinations(input_set, "2")  # type: ignore


def test_get_combinations_value_error_negative_r() -> None:
    """
    Test case 11: ValueError when r is negative.
    """
    # Arrange
    input_set = {1, 2, 3}

    # Act & Assert
    with pytest.raises(ValueError, match="r must be non-negative"):
        get_combinations(input_set, -1)


def test_get_combinations_value_error_r_too_large() -> None:
    """
    Test case 12: ValueError when r is larger than set size.
    """
    # Arrange
    input_set = {1, 2, 3}

    # Act & Assert
    with pytest.raises(ValueError, match="r cannot be larger than set size"):
        get_combinations(input_set, 5)
