import numpy as np
import pytest
from numpy_functions.array_median import array_median


def test_array_median_odd() -> None:
    """
    Test array_median with an odd number of elements.
    """
    assert array_median(np.array([1, 3, 5])
                        ) == 3.0, "Failed on odd number of elements"


def test_array_median_even() -> None:
    """
    Test array_median with an even number of elements.
    """
    assert array_median(np.array([1, 2, 3, 4])
                        ) == 2.5, "Failed on even number of elements"


def test_array_median_invalid_type() -> None:
    """
    Test array_median with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_median([1, 2, 3])
