import numpy as np
import pytest
from numpy_functions.array_std import array_std


def test_array_std_basic() -> None:
    """
    Test the array_std function with positive integers.
    """
    assert array_std(np.array([1, 2, 3, 4])) == float(
        np.std(np.array([1, 2, 3, 4]))
    ), "Failed on positive integers"


def test_array_std_negative() -> None:
    """
    Test the array_std function with negative numbers.
    """
    assert array_std(np.array([-1, -2, -3])) == float(
        np.std(np.array([-1, -2, -3]))
    ), "Failed on negative numbers"


def test_array_std_invalid_type() -> None:
    """
    Test the array_std function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_std([1, 2, 3])

