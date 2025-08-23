import numpy as np
import pytest
from numpy_functions.array_argmin import array_argmin


def test_array_argmin_basic() -> None:
    """
    Test the array_argmin function with positive integers.
    """
    assert array_argmin(np.array([1, 0, 2])
                        ) == 1, "Failed on positive integers"


def test_array_argmin_negative() -> None:
    """
    Test the array_argmin function with negative numbers.
    """
    assert array_argmin(np.array([-5, -1, -3])
                        ) == 0, "Failed on negative numbers"


def test_array_argmin_invalid_type() -> None:
    """
    Test the array_argmin function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_argmin([1, 2, 3])
