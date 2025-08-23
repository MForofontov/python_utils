import numpy as np
import pytest
from numpy_functions.elementwise_max import elementwise_max


def test_elementwise_max_basic() -> None:
    """
    Test elementwise_max with arrays of the same shape.
    """
    result = elementwise_max(np.array([1, 3]), np.array([2, 2]))
    expected = np.array([2, 3])
    assert np.array_equal(
        result, expected), "Failed on basic element-wise maximum"


def test_elementwise_max_mismatched_shapes() -> None:
    """
    Test elementwise_max with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_max(np.array([1, 2]), np.array([1, 2, 3]))


def test_elementwise_max_invalid_type() -> None:
    """
    Test elementwise_max with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_max([1, 2], np.array([1, 2]))
