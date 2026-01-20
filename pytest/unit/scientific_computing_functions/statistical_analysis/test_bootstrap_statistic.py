"""
Unit tests for bootstrap_statistic function.

Tests cover normal operation, edge cases, and error conditions.
"""

try:
    import numpy as np
    import scipy
    from pyutils_collection.scientific_computing_functions.statistical_analysis.bootstrap_statistic import (
        bootstrap_statistic,
    )
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None  # type: ignore
    scipy = None  # type: ignore
    bootstrap_statistic = None  # type: ignore

import pytest

pytestmark = pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy and/or scipy not installed")

pytestmark = pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy/scipy not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.scientific_computing]

# Normal operation tests


def test_bootstrap_statistic_mean_default() -> None:
    """Test case 1: Normal operation with mean statistic."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Act
    result = bootstrap_statistic(
        data, statistic="mean", n_iterations=1000, random_seed=42
    )

    # Assert
    assert "point_estimate" in result
    assert "ci_lower" in result
    assert "ci_upper" in result
    assert "standard_error" in result
    assert abs(result["point_estimate"] - 5.5) < 0.1
    assert result["ci_lower"] < result["point_estimate"] < result["ci_upper"]


def test_bootstrap_statistic_median() -> None:
    """Test case 2: Normal operation with median statistic."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Act
    result = bootstrap_statistic(
        data, statistic="median", n_iterations=1000, random_seed=42
    )

    # Assert
    assert abs(result["point_estimate"] - 5.5) < 0.1
    assert result["ci_lower"] < result["point_estimate"] < result["ci_upper"]


def test_bootstrap_statistic_std() -> None:
    """Test case 3: Normal operation with standard deviation statistic."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Act
    result = bootstrap_statistic(
        data, statistic="std", n_iterations=1000, random_seed=42
    )

    # Assert
    assert result["point_estimate"] > 0
    assert result["standard_error"] > 0
    assert result["ci_lower"] < result["ci_upper"]


def test_bootstrap_statistic_numpy_array() -> None:
    """Test case 4: Normal operation with numpy array input."""
    # Arrange
    data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

    # Act
    result = bootstrap_statistic(data, n_iterations=500, random_seed=42)

    # Assert
    assert abs(result["point_estimate"] - 3.0) < 0.1
    assert all(
        key in result
        for key in ["point_estimate", "ci_lower", "ci_upper", "standard_error"]
    )


def test_bootstrap_statistic_different_confidence_level() -> None:
    """Test case 5: Normal operation with 99% confidence level."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Act
    result_95 = bootstrap_statistic(
        data, confidence_level=0.95, n_iterations=1000, random_seed=42
    )
    result_99 = bootstrap_statistic(
        data, confidence_level=0.99, n_iterations=1000, random_seed=42
    )

    # Assert
    # 99% CI should be wider than 95% CI
    width_95 = result_95["ci_upper"] - result_95["ci_lower"]
    width_99 = result_99["ci_upper"] - result_99["ci_lower"]
    assert width_99 > width_95


def test_bootstrap_statistic_reproducible_with_seed() -> None:
    """Test case 6: Normal operation with random seed for reproducibility."""
    # Arrange
    data = [1, 2, 3, 4, 5]

    # Act
    result1 = bootstrap_statistic(data, random_seed=42, n_iterations=1000)
    result2 = bootstrap_statistic(data, random_seed=42, n_iterations=1000)

    # Assert
    assert result1["ci_lower"] == result2["ci_lower"]
    assert result1["ci_upper"] == result2["ci_upper"]


# Edge case tests


def test_bootstrap_statistic_small_dataset() -> None:
    """Test case 7: Edge case with small dataset (n=3)."""
    # Arrange
    data = [1.0, 2.0, 3.0]

    # Act
    result = bootstrap_statistic(data, n_iterations=100, random_seed=42)

    # Assert
    assert result["point_estimate"] == 2.0
    assert result["ci_lower"] < result["ci_upper"]


def test_bootstrap_statistic_single_iteration() -> None:
    """Test case 8: Edge case with minimum iterations (n=1)."""
    # Arrange
    data = [1, 2, 3, 4, 5]

    # Act
    result = bootstrap_statistic(data, n_iterations=1, random_seed=42)

    # Assert
    assert "standard_error" in result
    assert result["standard_error"] >= 0


def test_bootstrap_statistic_identical_values() -> None:
    """Test case 9: Edge case with all identical values."""
    # Arrange
    data = [5.0] * 10

    # Act
    result = bootstrap_statistic(data, n_iterations=500, random_seed=42)

    # Assert
    assert result["point_estimate"] == 5.0
    assert result["standard_error"] == 0.0


def test_bootstrap_statistic_high_variance_data() -> None:
    """Test case 10: Edge case with high variance data."""
    # Arrange
    data = [1, 100, 2, 99, 3, 98, 4, 97, 5, 96]

    # Act
    result = bootstrap_statistic(data, n_iterations=1000, random_seed=42)

    # Assert
    assert result["standard_error"] > 0
    # CI should be wide due to high variance
    assert (result["ci_upper"] - result["ci_lower"]) > 10


def test_bootstrap_statistic_large_dataset() -> None:
    """Test case 11: Edge case with large dataset."""
    # Arrange
    data = list(range(1000))

    # Act
    result = bootstrap_statistic(data, n_iterations=500, random_seed=42)

    # Assert
    assert abs(result["point_estimate"] - 499.5) < 1
    assert result["ci_lower"] < result["ci_upper"]


def test_bootstrap_statistic_many_iterations() -> None:
    """Test case 12: Edge case with many bootstrap iterations."""
    # Arrange
    data = [1, 2, 3, 4, 5]

    # Act
    result = bootstrap_statistic(data, n_iterations=50000, random_seed=42)

    # Assert
    # More iterations should give stable estimates
    assert result["standard_error"] > 0
    assert result["ci_lower"] < result["point_estimate"] < result["ci_upper"]


# Error case tests


def test_bootstrap_statistic_invalid_data_type() -> None:
    """Test case 13: TypeError for invalid data type."""
    # Arrange
    invalid_data = "not a list or array"
    expected_message = "data must be a list or numpy array"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        bootstrap_statistic(invalid_data)


def test_bootstrap_statistic_empty_data() -> None:
    """Test case 14: ValueError for empty data."""
    # Arrange
    empty_data = []
    expected_message = "data cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bootstrap_statistic(empty_data)


def test_bootstrap_statistic_invalid_statistic_type() -> None:
    """Test case 15: TypeError for invalid statistic type."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "statistic must be a string"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        bootstrap_statistic(data, statistic=123)


def test_bootstrap_statistic_invalid_statistic_value() -> None:
    """Test case 16: ValueError for invalid statistic value."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "statistic must be 'mean', 'median', or 'std'"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bootstrap_statistic(data, statistic="invalid")


def test_bootstrap_statistic_invalid_n_iterations_type() -> None:
    """Test case 17: TypeError for invalid n_iterations type."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "n_iterations must be an integer"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        bootstrap_statistic(data, n_iterations=100.5)


def test_bootstrap_statistic_negative_n_iterations() -> None:
    """Test case 18: ValueError for negative n_iterations."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "n_iterations must be >= 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bootstrap_statistic(data, n_iterations=-10)


def test_bootstrap_statistic_zero_n_iterations() -> None:
    """Test case 19: ValueError for zero n_iterations."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "n_iterations must be >= 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bootstrap_statistic(data, n_iterations=0)


def test_bootstrap_statistic_invalid_confidence_level_type() -> None:
    """Test case 20: TypeError for invalid confidence_level type."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "confidence_level must be a number"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        bootstrap_statistic(data, confidence_level="0.95")


def test_bootstrap_statistic_confidence_level_too_low() -> None:
    """Test case 21: ValueError for confidence_level <= 0."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "confidence_level must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bootstrap_statistic(data, confidence_level=0.0)


def test_bootstrap_statistic_confidence_level_too_high() -> None:
    """Test case 22: ValueError for confidence_level >= 1."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "confidence_level must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        bootstrap_statistic(data, confidence_level=1.0)


def test_bootstrap_statistic_invalid_random_seed_type() -> None:
    """Test case 23: TypeError for invalid random_seed type."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "random_seed must be an integer or None"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        bootstrap_statistic(data, random_seed="42")
