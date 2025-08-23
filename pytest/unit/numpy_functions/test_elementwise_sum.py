import numpy as np
import pytest
from numpy_functions.elementwise_sum import elementwise_sum


def test_elementwise_sum_basic() -> None:
    """
    Test elementwise_sum with arrays of the same shape.
    """
    result = elementwise_sum(np.array([1, 2]), np.array([3, 4]))
    expected = np.array([4, 6])
    assert np.array_equal(result, expected), "Failed on basic element-wise sum"


def test_elementwise_sum_mismatched_shapes() -> None:
    """
    Test elementwise_sum with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_sum(np.array([1, 2]), np.array([1, 2, 3]))


def test_elementwise_sum_invalid_type() -> None:
    """
    Test elementwise_sum with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_sum([1, 2], np.array([1, 2]))
