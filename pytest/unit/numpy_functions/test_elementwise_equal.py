import numpy as np
import pytest
from numpy_functions.elementwise_equal import elementwise_equal



def test_elementwise_equal_basic() -> None:
    """
    Test element-wise equality with simple arrays.
    """
    result = elementwise_equal(np.array([1, 2, 3]), np.array([1, 4, 3]))
    expected = np.array([True, False, True])
    np.testing.assert_array_equal(result, expected)



def test_elementwise_equal_invalid_type() -> None:
    """
    Test that passing non-array inputs raises TypeError.
    """
    with pytest.raises(TypeError):
        elementwise_equal([1, 2], np.array([1, 2]))



def test_elementwise_equal_shape_mismatch() -> None:
    """
    Test that shape mismatch raises ValueError.
    """
    with pytest.raises(ValueError):
        elementwise_equal(np.array([1, 2]), np.array([1, 2, 3]))
