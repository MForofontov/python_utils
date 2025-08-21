import numpy as np
import pytest
from numpy_functions.dot_product import dot_product


def test_dot_product_basic() -> None:
    """
    Test the dot_product function with basic one-dimensional arrays.
    """
    # Test case 1: Basic arrays
    assert dot_product(np.array([1, 2, 3]), np.array([4, 5, 6])) == 32.0, "Failed on basic arrays"


def test_dot_product_zero() -> None:
    """
    Test the dot_product function with arrays containing zeros.
    """
    # Test case 2: Arrays with zeros
    assert dot_product(np.array([0, 0]), np.array([0, 0])) == 0.0, "Failed on zero arrays"


def test_dot_product_mismatched_shapes() -> None:
    """
    Test the dot_product function with arrays of mismatched shapes.
    """
    # Test case 3: Mismatched shapes
    with pytest.raises(ValueError):
        dot_product(np.array([1, 2]), np.array([1, 2, 3]))


def test_dot_product_invalid_type() -> None:
    """
    Test the dot_product function with an invalid input type.
    """
    # Test case 4: Invalid input type
    with pytest.raises(TypeError):
        dot_product([1, 2, 3], np.array([1, 2, 3]))
