import numpy as np
import pytest
from numpy_functions.array_round import array_round


def test_array_round_default() -> None:
    """
    Test rounding with default decimals.
    """
    np.testing.assert_array_equal(array_round(
        np.array([1.2, 2.6])), np.array([1.0, 3.0]))


def test_array_round_decimals() -> None:
    """
    Test rounding with specified decimals.
    """
    result = array_round(np.array([1.234, 5.678]), 2)
    expected = np.array([1.23, 5.68])
    np.testing.assert_allclose(result, expected)


def test_array_round_invalid_input() -> None:
    """
    Test passing a non-array input raises TypeError.
    """
    with pytest.raises(TypeError):
        array_round([1.2, 2.3])


def test_array_round_invalid_decimals() -> None:
    """
    Test passing a non-integer decimals raises TypeError.
    """
    with pytest.raises(TypeError):
        array_round(np.array([1.2, 2.3]), 1.5)
