import numpy as np
import pytest
from numpy_functions.normalize_array import normalize_array


def test_normalize_array_basic() -> None:
    """
    Test normalize_array with a basic 1-D array.
    """
    result = normalize_array(np.array([3.0, 4.0]))
    expected = np.array([0.6, 0.8])
    assert np.allclose(result, expected), "Failed to normalize array correctly"


def test_normalize_array_zero_norm() -> None:
    """
    Test normalize_array with an array of zeros which has zero norm.
    """
    with pytest.raises(ValueError):
        normalize_array(np.array([0.0, 0.0]))


def test_normalize_array_invalid_type() -> None:
    """
    Test normalize_array with an invalid input type.
    """
    with pytest.raises(TypeError):
        normalize_array([1, 2, 3])
