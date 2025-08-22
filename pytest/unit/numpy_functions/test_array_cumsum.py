import numpy as np
import pytest
from numpy_functions.array_cumsum import array_cumsum



def test_array_cumsum_basic() -> None:
    """
    Test the array_cumsum function with positive integers.
    """
    assert np.array_equal(array_cumsum(np.array([1, 2, 3])), np.array([1, 3, 6])), "Failed on positive integers"



def test_array_cumsum_negative() -> None:
    """
    Test the array_cumsum function with negative numbers.
    """
    assert np.array_equal(array_cumsum(np.array([-1, -2, -3])), np.array([-1, -3, -6])), "Failed on negative numbers"



def test_array_cumsum_invalid_type() -> None:
    """
    Test the array_cumsum function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_cumsum([1, 2, 3])
