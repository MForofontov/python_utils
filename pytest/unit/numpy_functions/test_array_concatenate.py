import numpy as np
import pytest
from numpy_functions.array_concatenate import array_concatenate


def test_array_concatenate_basic() -> None:
    """
    Concatenating two one-dimensional arrays should join them along axis 0.
    """
    arr1 = np.array([1, 2])
    arr2 = np.array([3, 4])
    result = array_concatenate([arr1, arr2])
    expected = np.array([1, 2, 3, 4])
    np.testing.assert_array_equal(result, expected)


def test_array_concatenate_axis() -> None:
    """
    Concatenating two two-dimensional arrays along axis 1 should combine their columns.
    """
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[5, 6], [7, 8]])
    result = array_concatenate([arr1, arr2], axis=1)
    expected = np.array([[1, 2, 5, 6], [3, 4, 7, 8]])
    np.testing.assert_array_equal(result, expected)


def test_array_concatenate_type_error() -> None:
    """
    Passing a non-array within the sequence should raise ``TypeError``.
    """
    arr1 = np.array([1])
    with pytest.raises(TypeError):
        array_concatenate([arr1, [2]])


def test_array_concatenate_empty() -> None:
    """
    An empty sequence should raise ``ValueError``.
    """
    with pytest.raises(ValueError):
        array_concatenate([])

