import numpy as np
import pytest
from numpy_functions.elementwise_subtract import elementwise_subtract



def test_elementwise_subtract_basic() -> None:
    """
    Test elementwise_subtract with arrays of the same shape.
    """
    result = elementwise_subtract(np.array([5, 7]), np.array([2, 3]))
    expected = np.array([3, 4])
    assert np.array_equal(result, expected), "Failed on basic element-wise subtraction"



def test_elementwise_subtract_mismatched_shapes() -> None:
    """
    Test elementwise_subtract with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_subtract(np.array([1, 2]), np.array([1, 2, 3]))



def test_elementwise_subtract_invalid_type() -> None:
    """
    Test elementwise_subtract with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_subtract([1, 2], np.array([1, 2]))
