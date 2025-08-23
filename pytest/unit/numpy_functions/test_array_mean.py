import numpy as np
import pytest
from numpy_functions.array_mean import array_mean


def test_array_mean_basic() -> None:
    """
    Test the array_mean function with positive integers.
    """
    # Test case 1: Positive integers
    assert array_mean(np.array([1, 2, 3, 4])
                      ) == 2.5, "Failed on positive integers"


def test_array_mean_negative() -> None:
    """
    Test the array_mean function with negative numbers.
    """
    # Test case 2: Negative numbers
    assert array_mean(np.array([-1, -2, -3])) == - \
        2.0, "Failed on negative numbers"


def test_array_mean_invalid_type() -> None:
    """
    Test the array_mean function with an invalid input type.
    """
    # Test case 3: Invalid input type
    with pytest.raises(TypeError):
        array_mean([1, 2, 3])
