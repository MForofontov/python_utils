import numpy as np
import pytest
from numpy_functions.array_log import array_log


def test_array_log_basic() -> None:
    """
    Test the array_log function with positive numbers.
    """
    result = array_log(np.array([1.0, np.e]))
    expected = np.array([0.0, 1.0])
    assert np.allclose(result, expected), "Failed on basic logarithm"


def test_array_log_non_positive() -> None:
    """
    Test the array_log function when the array contains non-positive values.
    """
    with pytest.raises(ValueError):
        array_log(np.array([0.0, -1.0]))


def test_array_log_invalid_type() -> None:
    """
    Test the array_log function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_log([1.0, np.e])  # type: ignore[arg-type]
