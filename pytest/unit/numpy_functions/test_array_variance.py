import numpy as np
import pytest
from numpy_functions.array_variance import array_variance


def test_array_variance_basic() -> None:
    """
    Test the array_variance function with positive numbers.
    """
    assert array_variance(
        np.array([1, 3])) == 1.0, "Failed on positive numbers"


def test_array_variance_negative() -> None:
    """
    Test the array_variance function with negative numbers.
    """
    assert array_variance(
        np.array([-1, -3])) == 1.0, "Failed on negative numbers"


def test_array_variance_invalid_type() -> None:
    """
    Test the array_variance function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_variance([1, 2, 3])
