import numpy as np
import pytest
from numpy_functions.array_min import array_min


def test_array_min_basic() -> None:
    """
    Test the array_min function with positive integers.
    """
    assert array_min(np.array([1, 2, 3])) == 1.0, "Failed on positive integers"


def test_array_min_negative() -> None:
    """
    Test the array_min function with negative numbers.
    """
    assert array_min(np.array([-5, -2, -3])) == - \
        5.0, "Failed on negative numbers"


def test_array_min_invalid_type() -> None:
    """
    Test the array_min function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_min([1, 2, 3])
