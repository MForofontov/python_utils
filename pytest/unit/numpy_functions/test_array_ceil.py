import numpy as np
import pytest
from numpy_functions.array_ceil import array_ceil


def test_array_ceil_basic() -> None:
    """Test array_ceil with positive and negative decimals."""
    result = array_ceil(np.array([1.2, -2.7, 0.0]))
    expected = np.array([2.0, -2.0, 0.0])
    assert np.array_equal(result, expected), "Failed on basic ceil operation"


def test_array_ceil_invalid_type() -> None:
    """Test array_ceil with an invalid input type."""
    with pytest.raises(TypeError):
        array_ceil([1.2, -2.7])  # type: ignore[arg-type]
