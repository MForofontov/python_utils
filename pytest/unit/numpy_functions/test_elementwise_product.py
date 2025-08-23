import numpy as np
import pytest
from numpy_functions.elementwise_product import elementwise_product


def test_elementwise_product_basic() -> None:
    """
    Test elementwise_product with arrays of the same shape.
    """
    result = elementwise_product(np.array([1, 2]), np.array([3, 4]))
    expected = np.array([3, 8])
    assert np.array_equal(
        result, expected), "Failed on basic element-wise product"


def test_elementwise_product_mismatched_shapes() -> None:
    """
    Test elementwise_product with arrays of different shapes.
    """
    with pytest.raises(ValueError):
        elementwise_product(np.array([1, 2]), np.array([1, 2, 3]))


def test_elementwise_product_invalid_type() -> None:
    """
    Test elementwise_product with invalid input types.
    """
    with pytest.raises(TypeError):
        elementwise_product([1, 2], np.array([1, 2]))
