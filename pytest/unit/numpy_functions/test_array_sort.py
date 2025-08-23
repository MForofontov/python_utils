import numpy as np
import pytest
from numpy_functions.array_sort import array_sort


def test_array_sort_basic() -> None:
    """
    Test array_sort with positive integers.
    """
    assert np.array_equal(array_sort(np.array([3, 1, 2])), np.array(
        [1, 2, 3])), "Failed on positive integers"


def test_array_sort_negative() -> None:
    """
    Test array_sort with negative numbers.
    """
    assert np.array_equal(array_sort(
        np.array([-3, -1, -2])), np.array([-3, -2, -1])), "Failed on negative numbers"


def test_array_sort_invalid_type() -> None:
    """
    Test array_sort with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_sort([3, 1, 2])
