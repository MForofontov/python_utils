import numpy as np
import pytest
from numpy_functions.array_reshape import array_reshape


def test_array_reshape_basic() -> None:
    """
    Reshape a 1-D array into a 2-D array.
    """
    result = array_reshape(np.array([1, 2, 3, 4, 5, 6]), (2, 3))
    expected = np.array([[1, 2, 3], [4, 5, 6]])
    np.testing.assert_array_equal(result, expected)


def test_array_reshape_invalid_type() -> None:
    """
    Providing non-ndarray input should raise ``TypeError``.
    """
    with pytest.raises(TypeError):
        array_reshape([1, 2, 3], (3, 1))


def test_array_reshape_invalid_shape() -> None:
    """
    Incompatible new shape should raise ``ValueError``.
    """
    with pytest.raises(ValueError):
        array_reshape(np.array([1, 2, 3]), (2, 2))
