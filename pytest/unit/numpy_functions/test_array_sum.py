import numpy as np
import pytest
from numpy_functions.array_sum import array_sum


def test_array_sum_basic() -> None:
    """
    Test the array_sum function with positive integers.
    """
    assert array_sum(np.array([1, 2, 3])) == 6.0, "Failed on positive integers"


def test_array_sum_negative() -> None:
    """
    Test the array_sum function with negative numbers.
    """
    assert array_sum(np.array([-1, -2, -3])) == - \
        6.0, "Failed on negative numbers"


def test_array_sum_invalid_type() -> None:
    """
    Test the array_sum function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_sum([1, 2, 3])
