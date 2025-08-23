import numpy as np
import pytest
from numpy_functions.elementwise_less import elementwise_less



def test_elementwise_less_basic() -> None:
    """
    Basic element-wise less comparison between two arrays.
    """
    result = elementwise_less(np.array([1, 2, 3]), np.array([2, 2, 4]))
    expected = np.array([True, False, True])
    np.testing.assert_array_equal(result, expected)



def test_elementwise_less_invalid_type() -> None:
    """
    Providing non-ndarray inputs should raise ``TypeError``.
    """
    with pytest.raises(TypeError):
        elementwise_less([1, 2], np.array([1, 2]))



def test_elementwise_less_shape_mismatch() -> None:
    """
    Arrays with different shapes should raise ``ValueError``.
    """
    with pytest.raises(ValueError):
        elementwise_less(np.array([1, 2]), np.array([1, 2, 3]))
