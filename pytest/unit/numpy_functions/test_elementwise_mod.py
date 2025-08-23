import numpy as np
import pytest
from numpy_functions.elementwise_mod import elementwise_mod



def test_elementwise_mod_basic() -> None:
    """
    Test elementwise_mod with arrays of the same shape.
    """
    result = elementwise_mod(np.array([5, 7]), np.array([2, 3]))
    expected = np.array([1, 1])
    assert np.array_equal(result, expected), "Failed on basic element-wise modulus"



def test_elementwise_mod_mismatched_shapes() -> None:
    """
    Test elementwise_mod with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_mod(np.array([1, 2]), np.array([1, 2, 3]))



def test_elementwise_mod_invalid_type() -> None:
    """
    Test elementwise_mod with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_mod([1, 2], np.array([1, 2]))
