import numpy as np
import pytest
from numpy_functions.array_clip import array_clip


def test_array_clip_basic() -> None:
    """Test array_clip with values outside the clip range."""
    result = array_clip(np.array([1, 2, 3, 4]), 2, 3)
    expected = np.array([2, 2, 3, 3])
    assert np.array_equal(result, expected), "Failed to clip array within range"


def test_array_clip_invalid_type() -> None:
    """Test array_clip with invalid array type."""
    with pytest.raises(TypeError):
        array_clip([1, 2, 3], 0, 1)


def test_array_clip_invalid_bounds() -> None:
    """Test array_clip with min_value greater than max_value."""
    with pytest.raises(ValueError):
        array_clip(np.array([1, 2, 3]), 5, 1)
