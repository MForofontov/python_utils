import numpy as np
import pytest
from numpy_functions.elementwise_divide import elementwise_divide


def test_elementwise_divide_basic() -> None:
    """
    Test elementwise_divide with arrays of the same shape.
    """
    result = elementwise_divide(np.array([4, 6]), np.array([2, 3]))
    expected = np.array([2.0, 2.0])
    assert np.array_equal(
        result, expected
    ), "Failed on basic element-wise division"


def test_elementwise_divide_mismatched_shapes() -> None:
    """
    Test elementwise_divide with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_divide(np.array([1, 2]), np.array([1, 2, 3]))


def test_elementwise_divide_zero_division() -> None:
    """
    Test elementwise_divide when the denominator contains zero.
    """
    with pytest.raises(ValueError):
        elementwise_divide(np.array([1, 2]), np.array([0, 1]))


def test_elementwise_divide_invalid_type() -> None:
    """
    Test elementwise_divide with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_divide([1, 2], np.array([1, 2]))
