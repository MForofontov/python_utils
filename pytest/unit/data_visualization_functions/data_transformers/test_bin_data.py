"""
Unit tests for bin_data function.
"""

import matplotlib
import numpy as np

import pytest

matplotlib.use("Agg")  # Use non-GUI backend for testing
from data_visualization_functions.data_transformers.bin_data import bin_data


def test_bin_data_basic():
    """
    Test case 1: Bin data with default settings.
    """
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Act
    binned_indices, bin_edges = bin_data(data, bins=5)

    # Assert
    assert len(bin_edges) == 6  # bins + 1 edges
    assert len(binned_indices) == len(data)


def test_bin_data_custom_bins():
    """
    Test case 2: Bin data with custom number of bins.
    """
    # Arrange
    data = np.random.randn(1000)

    # Act
    binned_indices, bin_edges = bin_data(data, bins=20)

    # Assert
    assert len(bin_edges) == 21
    assert len(binned_indices) == len(data)


def test_bin_data_custom_bin_edges():
    """
    Test case 3: Bin data with custom bin edges.
    """
    # Arrange
    data = [1, 2, 3, 4, 5]
    custom_edges = [0, 2, 4, 6]

    # Act
    binned_indices, bin_edges = bin_data(data, bins=custom_edges)

    # Assert
    assert len(bin_edges) == len(custom_edges)


def test_bin_data_numpy_array():
    """
    Test case 4: Bin numpy array data.
    """
    # Arrange
    data = np.array([1.5, 2.5, 3.5, 4.5, 5.5])

    # Act
    binned_indices, bin_edges = bin_data(data, bins=5)

    # Assert
    assert isinstance(bin_edges, np.ndarray)
    assert isinstance(binned_indices, np.ndarray)


def test_bin_data_empty_raises_error():
    """
    Test case 5: ValueError for empty data.
    """
    # Arrange
    expected_message = "data cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bin_data([])


def test_bin_data_invalid_bins_raises_error():
    """
    Test case 6: ValueError for invalid number of bins.
    """
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "bins must be positive"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bin_data(data, bins=0)


def test_bin_data_invalid_type_raises_error():
    """
    Test case 7: TypeError for invalid data type.
    """
    # Arrange
    expected_message = "Cannot convert|could not convert|must be"

    # Act & Assert
    with pytest.raises((TypeError, ValueError), match=expected_message):
        bin_data("not_a_list")


def test_bin_data_single_value():
    """
    Test case 8: Bin data with single unique value.
    """
    # Arrange
    data = [5, 5, 5, 5, 5]

    # Act
    binned_indices, bin_edges = bin_data(data, bins=3)

    # Assert
    assert len(binned_indices) == len(data)


__all__ = ["test_bin_data_basic"]
