import numpy as np
import pytest
from numpy_functions.array_sqrt import array_sqrt


def test_array_sqrt_basic() -> None:
    """
    Test array_sqrt with non-negative numbers.
    """
    result = array_sqrt(np.array([0, 1, 4]))
    expected = np.array([0.0, 1.0, 2.0])
    assert np.array_equal(result, expected), "Failed on basic square root"


def test_array_sqrt_negative_values() -> None:
    """
    Test array_sqrt when the array contains negative values.
    """
    with pytest.raises(ValueError):
        array_sqrt(np.array([-1, 0]))


def test_array_sqrt_invalid_type() -> None:
    """
    Test array_sqrt with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_sqrt([0, 1, 4])  # type: ignore[arg-type]

