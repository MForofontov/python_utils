import numpy as np
import pytest
from numpy_functions.array_clip import array_clip


def test_array_clip_basic() -> None:
    """
    Test array_clip with values outside the specified range.
    """
    result = array_clip(np.array([-1, 2, 5]), 0, 4)
    expected = np.array([0, 2, 4])
    assert np.array_equal(result, expected), "Failed to clip array values"


def test_array_clip_invalid_type() -> None:
    """
    Test array_clip with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_clip([-1, 2, 5], 0, 4)  # type: ignore[arg-type]


def test_array_clip_invalid_range() -> None:
    """
    Test array_clip when a_min is greater than a_max.
    """
    with pytest.raises(ValueError):
        array_clip(np.array([1, 2, 3]), 5, 1)
