import numpy as np
import pytest
from numpy_functions.matrix_multiply import matrix_multiply


def test_matrix_multiply_basic() -> None:
    """
    Test matrix_multiply with compatible 2-D arrays.
    """
    result = matrix_multiply(np.array([[1, 2], [3, 4]]), np.array([[5], [6]]))
    expected = np.array([[17], [39]])
    assert np.array_equal(result, expected), "Failed on basic matrix multiplication"


def test_matrix_multiply_mismatched_shapes() -> None:
    """
    Test matrix_multiply with arrays that have incompatible shapes.
    """
    with pytest.raises(ValueError):
        matrix_multiply(np.array([[1, 2], [3, 4]]), np.array([[1, 2, 3]]))


def test_matrix_multiply_invalid_type() -> None:
    """
    Test matrix_multiply with invalid input types.
    """
    with pytest.raises(TypeError):
        matrix_multiply([[1, 2]], np.array([[1], [2]]))
