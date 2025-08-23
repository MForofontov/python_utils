import numpy as np
import pytest
from numpy_functions.array_exp import array_exp


def test_array_exp_basic() -> None:
    """
    Test the array_exp function with simple values.
    """
    result = array_exp(np.array([0, 1]))
    expected = np.array([1.0, np.e])
    assert np.allclose(result, expected), "Failed on basic exponential"


def test_array_exp_invalid_type() -> None:
    """
    Test the array_exp function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_exp([0, 1])  # type: ignore[arg-type]
