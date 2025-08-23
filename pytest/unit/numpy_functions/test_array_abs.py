import numpy as np
import pytest
from numpy_functions.array_abs import array_abs


def test_array_abs_basic() -> None:
    """
    Test the array_abs function with mixed positive and negative values.
    """
    result = array_abs(np.array([-1, 2, -3]))
    expected = np.array([1, 2, 3])
    assert np.array_equal(result, expected), "Failed on mixed values"


def test_array_abs_invalid_type() -> None:
    """
    Test the array_abs function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_abs([-1, 2, -3])
