import numpy as np
import pytest
from numpy_functions.array_percentile import array_percentile



def test_array_percentile_basic() -> None:
    """
    Test array_percentile with a simple array.
    """
    assert (
        array_percentile(np.array([1, 2, 3, 4]), 50) == 2.5
    ), "Failed on basic percentile"



def test_array_percentile_invalid_q_value() -> None:
    """
    Test array_percentile with an invalid percentile value.
    """
    with pytest.raises(ValueError):
        array_percentile(np.array([1, 2, 3]), 150)



def test_array_percentile_invalid_type() -> None:
    """
    Test array_percentile with invalid input types.
    """
    with pytest.raises(TypeError):
        array_percentile([1, 2, 3], 50)
    with pytest.raises(TypeError):
        array_percentile(np.array([1, 2, 3]), "50")
