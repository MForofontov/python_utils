import numpy as np
import pytest
from numpy_functions.elementwise_min import elementwise_min


def test_elementwise_min_basic() -> None:
    """
    Test elementwise_min with arrays of the same shape.
    """
    result = elementwise_min(np.array([1, 3]), np.array([2, 2]))
    expected = np.array([1, 2])
    assert np.array_equal(
        result, expected), "Failed on basic element-wise minimum"


def test_elementwise_min_mismatched_shapes() -> None:
    """
    Test elementwise_min with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_min(np.array([1, 2]), np.array([1, 2, 3]))


def test_elementwise_min_invalid_type() -> None:
    """
    Test elementwise_min with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_min([1, 2], np.array([1, 2]))
