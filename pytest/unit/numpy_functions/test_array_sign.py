import numpy as np
import pytest
from numpy_functions.array_sign import array_sign


def test_array_sign_basic() -> None:
    """Test array_sign with negative, zero, and positive values."""
    result = array_sign(np.array([-2.5, 0.0, 3.1]))
    expected = np.array([-1.0, 0.0, 1.0])
    assert np.array_equal(result, expected), "Failed on basic sign operation"


def test_array_sign_invalid_type() -> None:
    """Test array_sign with an invalid input type."""
    with pytest.raises(TypeError):
        array_sign([-2.5, 0.0, 3.1])  # type: ignore[arg-type]
