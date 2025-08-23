import numpy as np
import pytest
from numpy_functions.array_diff import array_diff


def test_array_diff_basic() -> None:
    """
    Test the array_diff function with increasing numbers.
    """
    assert np.array_equal(array_diff(np.array([1, 4, 9])), np.array(
        [3, 5])), "Failed on increasing numbers"


def test_array_diff_single_element() -> None:
    """
    Test the array_diff function with a single element array.
    """
    assert array_diff(
        np.array([42])).size == 0, "Failed on single element array"


def test_array_diff_invalid_type() -> None:
    """
    Test the array_diff function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_diff([1, 2])
