"""
Unit tests for correlation_analysis function.

Tests cover normal operation, edge cases, and error conditions.
"""

try:
    import numpy as np
    from python_utils.scientific_computing_functions.statistical_analysis.correlation_analysis import (
        correlation_analysis,
    )

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None  # type: ignore
    correlation_analysis = None  # type: ignore

import pytest

pytestmark = pytest.mark.skipif(not NUMPY_AVAILABLE, reason="numpy not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.scientific_computing]

# Normal operation tests


def test_correlation_analysis_pearson_positive() -> None:
    """Test case 1: Normal operation with positive Pearson correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    # Act
    result = correlation_analysis(x, y, method="pearson")

    # Assert
    assert result["correlation"] == pytest.approx(1.0, abs=0.01)
    assert result["pvalue"] < 0.05
    assert result["significant"]
    assert result["method"] == "pearson"
    assert result["interpretation"] == "strong"


def test_correlation_analysis_pearson_negative() -> None:
    """Test case 2: Normal operation with negative correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]

    # Act
    result = correlation_analysis(x, y, method="pearson")

    # Assert
    assert result["correlation"] < 0
    assert abs(result["correlation"]) == pytest.approx(1.0, abs=0.01)
    assert result["significant"]


def test_correlation_analysis_spearman() -> None:
    """Test case 3: Normal operation with Spearman correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]  # Non-linear but monotonic

    # Act
    result = correlation_analysis(x, y, method="spearman")

    # Assert
    assert result["correlation"] == pytest.approx(1.0, abs=0.01)
    assert result["method"] == "spearman"


def test_correlation_analysis_kendall() -> None:
    """Test case 4: Normal operation with Kendall correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4, 5, 6]

    # Act
    result = correlation_analysis(x, y, method="kendall")

    # Assert
    assert result["correlation"] > 0.9
    assert result["method"] == "kendall"


def test_correlation_analysis_numpy_arrays() -> None:
    """Test case 5: Normal operation with numpy arrays."""
    # Arrange
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.5, 3.5, 4.5, 5.5, 6.5])

    # Act
    result = correlation_analysis(x, y)

    # Assert
    assert result["correlation"] == pytest.approx(1.0, abs=0.01)
    assert "pvalue" in result


def test_correlation_analysis_not_significant() -> None:
    """Test case 6: Normal operation with non-significant correlation."""
    # Arrange
    np.random.seed(42)
    x = np.random.randn(10)
    y = np.random.randn(10)

    # Act
    result = correlation_analysis(x, y, alpha=0.05)

    # Assert
    assert "significant" in result
    assert isinstance(result["significant"], (bool, np.bool_))


# Edge case tests


def test_correlation_analysis_no_correlation() -> None:
    """Test case 7: Edge case with zero correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [3, 3, 3, 3, 3]  # Constant, no correlation

    # Act
    result = correlation_analysis(x, y)

    # Assert - constant y results in NaN correlation
    assert np.isnan(result["correlation"])
    assert np.isnan(result["pvalue"])


def test_correlation_analysis_small_dataset() -> None:
    """Test case 8: Edge case with minimum dataset size (n=3)."""
    # Arrange
    x = [1.0, 2.0, 3.0]
    y = [2.0, 4.0, 6.0]

    # Act
    result = correlation_analysis(x, y)

    # Assert
    assert result["correlation"] == pytest.approx(1.0, abs=0.01)


def test_correlation_analysis_moderate_correlation() -> None:
    """Test case 9: Edge case with moderate correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 4, 5, 4, 6, 7, 8, 9, 8, 11]

    # Act
    result = correlation_analysis(x, y)

    # Assert
    assert 0.3 < abs(result["correlation"]) < 1.0
    assert result["interpretation"] in ["moderate", "strong"]


def test_correlation_analysis_weak_correlation() -> None:
    """Test case 10: Edge case with weak correlation."""
    # Arrange
    np.random.seed(42)
    x = np.arange(100)
    y = x + np.random.randn(100) * 50  # Large noise

    # Act
    result = correlation_analysis(x, y)

    # Assert
    assert 0 < result["correlation"] < 0.7
    assert result["interpretation"] in ["weak", "moderate"]


def test_correlation_analysis_perfect_negative() -> None:
    """Test case 11: Edge case with perfect negative correlation."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [5, 4, 3, 2, 1]

    # Act
    result = correlation_analysis(x, y)

    # Assert
    assert result["correlation"] == pytest.approx(-1.0, abs=0.01)
    assert result["interpretation"] == "strong"


def test_correlation_analysis_strict_alpha() -> None:
    """Test case 12: Edge case with strict significance level."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 4, 5, 6]

    # Act
    result = correlation_analysis(x, y, alpha=0.001)

    # Assert
    assert "significant" in result
    assert isinstance(result["pvalue"], float)


# Error case tests


def test_correlation_analysis_invalid_x_type() -> None:
    """Test case 13: TypeError for invalid x type."""
    # Arrange
    invalid_x = "not a list or array"
    y = [1, 2, 3]
    expected_message = "x must be a list or numpy array"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        correlation_analysis(invalid_x, y)


def test_correlation_analysis_invalid_y_type() -> None:
    """Test case 14: TypeError for invalid y type."""
    # Arrange
    x = [1, 2, 3]
    invalid_y = {"not": "valid"}
    expected_message = "y must be a list or numpy array"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        correlation_analysis(x, invalid_y)


def test_correlation_analysis_empty_x() -> None:
    """Test case 15: ValueError for empty x."""
    # Arrange
    empty_x = []
    y = [1, 2, 3]
    expected_message = "x cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(empty_x, y)


def test_correlation_analysis_empty_y() -> None:
    """Test case 16: ValueError for empty y."""
    # Arrange
    x = [1, 2, 3]
    empty_y = []
    expected_message = "y cannot be empty"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(x, empty_y)


def test_correlation_analysis_mismatched_lengths() -> None:
    """Test case 17: ValueError for mismatched array lengths."""
    # Arrange
    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3]
    expected_message = "x and y must have the same length"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(x, y)


def test_correlation_analysis_invalid_method_type() -> None:
    """Test case 18: TypeError for invalid method type."""
    # Arrange
    x = [1, 2, 3]
    y = [2, 3, 4]
    expected_message = "method must be a string"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        correlation_analysis(x, y, method=123)


def test_correlation_analysis_invalid_method_value() -> None:
    """Test case 19: ValueError for invalid method value."""
    # Arrange
    x = [1, 2, 3]
    y = [2, 3, 4]
    expected_message = "method must be 'pearson', 'spearman', or 'kendall'"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(x, y, method="invalid")


def test_correlation_analysis_invalid_alpha_type() -> None:
    """Test case 20: TypeError for invalid alpha type."""
    # Arrange
    x = [1, 2, 3]
    y = [2, 3, 4]
    expected_message = "alpha must be a number"

    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        correlation_analysis(x, y, alpha="0.05")


def test_correlation_analysis_alpha_out_of_range_low() -> None:
    """Test case 21: ValueError for alpha <= 0."""
    # Arrange
    x = [1, 2, 3]
    y = [2, 3, 4]
    expected_message = "alpha must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(x, y, alpha=0.0)


def test_correlation_analysis_alpha_out_of_range_high() -> None:
    """Test case 22: ValueError for alpha >= 1."""
    # Arrange
    x = [1, 2, 3]
    y = [2, 3, 4]
    expected_message = "alpha must be between 0 and 1"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(x, y, alpha=1.0)


def test_correlation_analysis_non_numeric_x() -> None:
    """Test case 23: ValueError for non-numeric x."""
    # Arrange
    invalid_x = ["a", "b", "c"]
    y = [1, 2, 3]
    expected_message = "arrays contain non-numeric values"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(invalid_x, y)


def test_correlation_analysis_non_numeric_y() -> None:
    """Test case 24: ValueError for non-numeric y."""
    # Arrange
    x = [1, 2, 3]
    invalid_y = ["x", "y", "z"]
    expected_message = "arrays contain non-numeric values"

    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        correlation_analysis(x, invalid_y)
