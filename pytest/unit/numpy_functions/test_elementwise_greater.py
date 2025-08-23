import numpy as np
import pytest
from numpy_functions.elementwise_greater import elementwise_greater


def test_elementwise_greater_basic() -> None:
    """
    Basic element-wise greater comparison between two arrays.
    """
    result = elementwise_greater(np.array([2, 3, 4]), np.array([1, 3, 2]))
    expected = np.array([True, False, True])
    np.testing.assert_array_equal(result, expected)


def test_elementwise_greater_invalid_type() -> None:
    """
    Providing non-ndarray inputs should raise ``TypeError``.
    """
    with pytest.raises(TypeError):
        elementwise_greater([1, 2], np.array([1, 2]))


def test_elementwise_greater_shape_mismatch() -> None:
    """
    Arrays with different shapes should raise ``ValueError``.
    """
    with pytest.raises(ValueError):
        elementwise_greater(np.array([1, 2]), np.array([1, 2, 3]))
