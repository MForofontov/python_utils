import numpy as np
import pytest
from numpy_functions.array_unique import array_unique


def test_array_unique_basic() -> None:
    """
    Test array_unique with duplicate elements.
    """
    result = array_unique(np.array([1, 2, 2, 3]))
    expected = np.array([1, 2, 3])
    assert np.array_equal(result, expected), "Failed on duplicate elements"


def test_array_unique_unsorted() -> None:
    """
    Test array_unique with unsorted input.
    """
    result = array_unique(np.array([3, 1, 2, 2]))
    expected = np.array([1, 2, 3])
    assert np.array_equal(result, expected), "Failed on unsorted input"


def test_array_unique_invalid_type() -> None:
    """
    Test array_unique with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_unique([1, 2, 2, 3])
