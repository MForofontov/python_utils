import numpy as np
import pytest
from numpy_functions.array_floor import array_floor


def test_array_floor_basic() -> None:
    """
    Test array_floor with positive and negative decimal numbers.
    """
    result = array_floor(np.array([1.7, -2.3, 0.0]))
    expected = np.array([1.0, -3.0, 0.0])
    assert np.array_equal(result, expected), "Failed on basic floor operation"


def test_array_floor_invalid_type() -> None:
    """
    Test array_floor with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_floor([1.7, -2.3])  # type: ignore[arg-type]
