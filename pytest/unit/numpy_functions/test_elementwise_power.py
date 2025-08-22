import numpy as np
import pytest
from numpy_functions.elementwise_power import elementwise_power



def test_elementwise_power_basic() -> None:
    """
    Test elementwise_power with arrays of the same shape.
    """
    result = elementwise_power(np.array([2, 3]), np.array([3, 2]))
    expected = np.array([8, 9])
    assert np.array_equal(result, expected), "Failed on basic element-wise power"



def test_elementwise_power_mismatched_shapes() -> None:
    """
    Test elementwise_power with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_power(np.array([1, 2]), np.array([1]))



def test_elementwise_power_invalid_type() -> None:
    """
    Test elementwise_power with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_power([1, 2], np.array([1, 2]))
