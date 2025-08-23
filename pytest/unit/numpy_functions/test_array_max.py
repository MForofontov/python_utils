import numpy as np
import pytest
from numpy_functions.array_max import array_max


def test_array_max_basic() -> None:
    """
    Test the array_max function with positive integers.
    """
    assert array_max(np.array([1, 2, 3])) == 3.0, "Failed on positive integers"


def test_array_max_negative() -> None:
    """
    Test the array_max function with negative numbers.
    """
    assert array_max(np.array([-5, -2, -3])) == - \
        2.0, "Failed on negative numbers"


def test_array_max_invalid_type() -> None:
    """
    Test the array_max function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_max([1, 2, 3])
