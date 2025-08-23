import numpy as np
import pytest
from numpy_functions.array_argmax import array_argmax


def test_array_argmax_basic() -> None:
    """
    Test the array_argmax function with positive integers.
    """
    assert array_argmax(np.array([1, 3, 2])
                        ) == 1, "Failed on positive integers"


def test_array_argmax_negative() -> None:
    """
    Test the array_argmax function with negative numbers.
    """
    assert array_argmax(np.array([-5, -1, -3])
                        ) == 1, "Failed on negative numbers"


def test_array_argmax_invalid_type() -> None:
    """
    Test the array_argmax function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_argmax([1, 2, 3])
