import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from pyutils_collection.testing_functions.assertion_helpers.assert_list_equal_unordered import (
    assert_list_equal_unordered,
)


def test_assert_list_equal_unordered_equal_ordered() -> None:
    """
    Test case 1: Assert lists that are equal and ordered.
    """
    # Act & Assert
    assert_list_equal_unordered([1, 2, 3], [1, 2, 3])


def test_assert_list_equal_unordered_equal_unordered() -> None:
    """
    Test case 2: Assert lists that are equal but unordered.
    """
    # Act & Assert
    assert_list_equal_unordered([1, 2, 3], [3, 2, 1])


def test_assert_list_equal_unordered_string_lists() -> None:
    """
    Test case 3: Assert string lists ignoring order.
    """
    # Act & Assert
    assert_list_equal_unordered(["a", "b", "c"], ["c", "b", "a"])


def test_assert_list_equal_unordered_empty_lists() -> None:
    """
    Test case 4: Assert empty lists.
    """
    # Act & Assert
    assert_list_equal_unordered([], [])


def test_assert_list_equal_unordered_single_element() -> None:
    """
    Test case 5: Assert single element lists.
    """
    # Act & Assert
    assert_list_equal_unordered([42], [42])


def test_assert_list_equal_unordered_duplicates() -> None:
    """
    Test case 6: Assert lists with duplicate elements.
    """
    # Act & Assert
    assert_list_equal_unordered([1, 2, 2, 3], [3, 2, 1, 2])


def test_assert_list_equal_unordered_type_error_actual() -> None:
    """
    Test case 7: TypeError for invalid actual type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="actual must be a list"):
        assert_list_equal_unordered("not a list", [1, 2, 3])


def test_assert_list_equal_unordered_type_error_expected() -> None:
    """
    Test case 8: TypeError for invalid expected type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="expected must be a list"):
        assert_list_equal_unordered([1, 2, 3], "not a list")


def test_assert_list_equal_unordered_assertion_error_different_lengths() -> None:
    """
    Test case 9: AssertionError for different lengths.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Lists have different lengths"):
        assert_list_equal_unordered([1, 2], [1, 2, 3])


def test_assert_list_equal_unordered_assertion_error_different_elements() -> None:
    """
    Test case 10: AssertionError for different elements.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Lists contain different elements"):
        assert_list_equal_unordered([1, 2, 3], [1, 2, 4])
