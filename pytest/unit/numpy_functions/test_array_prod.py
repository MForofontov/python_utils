import numpy as np
import pytest
from numpy_functions.array_prod import array_prod


def test_array_prod_basic() -> None:
    """
    Test the array_prod function with positive integers.
    """
    assert array_prod(np.array([1, 2, 3])
                      ) == 6.0, "Failed on positive integers"


def test_array_prod_negative() -> None:
    """
    Test the array_prod function with negative numbers.
    """
    assert array_prod(np.array([-1, -2, -3])) == - \
        6.0, "Failed on negative numbers"


def test_array_prod_invalid_type() -> None:
    """
    Test the array_prod function with an invalid input type.
    """
    with pytest.raises(TypeError):
        array_prod([1, 2, 3])
