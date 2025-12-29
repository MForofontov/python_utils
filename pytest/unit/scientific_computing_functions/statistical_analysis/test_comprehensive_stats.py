"""
Unit tests for comprehensive_stats function.

Tests cover normal operation, edge cases, and error conditions.
"""

import pytest
import numpy as np
from scientific_computing_functions.statistical_analysis.comprehensive_stats import (
    comprehensive_stats,
)


# Normal operation tests


def test_comprehensive_stats_basic_dataset() -> None:
    """Test case 1: Normal operation with basic dataset."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert result['mean'] == 5.5
    assert result['median'] == 5.5
    assert result['std'] > 0
    assert 'skewness' in result
    assert 'kurtosis' in result


def test_comprehensive_stats_with_distribution_tests() -> None:
    """Test case 2: Normal operation including distribution tests."""
    # Arrange
    data = np.random.normal(0, 1, 100)
    np.random.seed(42)
    data = np.random.normal(0, 1, 100)
    
    # Act
    result = comprehensive_stats(data, include_distribution_tests=True)
    
    # Assert
    assert 'shapiro_statistic' in result
    assert 'shapiro_pvalue' in result
    assert 'jarque_bera_statistic' in result
    assert 'jarque_bera_pvalue' in result


def test_comprehensive_stats_without_distribution_tests() -> None:
    """Test case 3: Normal operation excluding distribution tests."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    
    # Act
    result = comprehensive_stats(data, include_distribution_tests=False)
    
    # Assert
    assert 'normality_test' not in result
    assert 'mean' in result
    assert 'median' in result


def test_comprehensive_stats_numpy_array() -> None:
    """Test case 4: Normal operation with numpy array."""
    # Arrange
    data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert result['mean'] == 30.0
    assert result['median'] == 30.0
    assert result['range'] == 40.0


def test_comprehensive_stats_with_outliers() -> None:
    """Test case 5: Normal operation with outliers."""
    # Arrange
    data = [1, 2, 3, 4, 5, 100]  # 100 is an outlier
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert 'n_outliers' in result
    assert result['n_outliers'] >= 1  # At least one outlier
    assert result['mean'] > result['median']  # Mean pulled by outlier


def test_comprehensive_stats_different_confidence_level() -> None:
    """Test case 6: Normal operation with 99% confidence level."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Act
    result = comprehensive_stats(data, confidence_level=0.99)
    
    # Assert
    assert 'ci_lower' in result
    assert 'ci_upper' in result
    assert result['ci_lower'] < result['mean'] < result['ci_upper']


# Edge case tests


def test_comprehensive_stats_small_dataset() -> None:
    """Test case 7: Edge case with small dataset (n=3)."""
    # Arrange
    data = [1.0, 2.0, 3.0]
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert result['mean'] == 2.0
    assert result['median'] == 2.0
    assert 'std' in result


def test_comprehensive_stats_identical_values() -> None:
    """Test case 8: Edge case with all identical values."""
    # Arrange
    data = [5.0] * 10
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert result['mean'] == 5.0
    assert result['median'] == 5.0
    assert result['std'] == 0.0
    assert result['variance'] == 0.0
    assert result['range'] == 0.0


def test_comprehensive_stats_with_nan_values() -> None:
    """Test case 9: Edge case with NaN values (should be removed with warning)."""
    # Arrange
    data = [1.0, 2.0, np.nan, 4.0, 5.0]
    
    # Act
    with pytest.warns(UserWarning, match="data contains 1 NaN value"):
        result = comprehensive_stats(data)
    
    # Assert
    assert result['n'] == 4  # NaN removed
    assert result['mean'] == 3.0


def test_comprehensive_stats_high_skewness() -> None:
    """Test case 10: Edge case with highly skewed data."""
    # Arrange
    data = [1] * 50 + [100]  # Highly right-skewed
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert result['skewness'] > 1  # Positive skew
    assert result['mean'] > result['median']


def test_comprehensive_stats_negative_values() -> None:
    """Test case 11: Edge case with negative values."""
    # Arrange
    data = [-10, -5, 0, 5, 10]
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert result['mean'] == 0.0
    assert result['median'] == 0.0
    assert result['range'] == 20.0


def test_comprehensive_stats_large_dataset() -> None:
    """Test case 12: Edge case with large dataset."""
    # Arrange
    np.random.seed(42)
    data = np.random.randn(10000)
    
    # Act
    result = comprehensive_stats(data)
    
    # Assert
    assert abs(result['mean']) < 0.1  # Should be close to 0
    assert abs(result['std'] - 1.0) < 0.1  # Should be close to 1


# Error case tests


def test_comprehensive_stats_invalid_data_type() -> None:
    """Test case 13: TypeError for invalid data type."""
    # Arrange
    invalid_data = "not a list or array"
    expected_message = "data must be a list or numpy array"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        comprehensive_stats(invalid_data)


def test_comprehensive_stats_empty_data() -> None:
    """Test case 14: ValueError for empty data."""
    # Arrange
    empty_data = []
    expected_message = "data cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        comprehensive_stats(empty_data)


def test_comprehensive_stats_non_numeric_data() -> None:
    """Test case 15: ValueError for non-numeric data."""
    # Arrange
    invalid_data = ["a", "b", "c"]
    expected_message = "data contains non-numeric values"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        comprehensive_stats(invalid_data)


def test_comprehensive_stats_invalid_confidence_level_type() -> None:
    """Test case 16: TypeError for invalid confidence_level type."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "confidence_level must be a number"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        comprehensive_stats(data, confidence_level="0.95")


def test_comprehensive_stats_confidence_level_too_low() -> None:
    """Test case 17: ValueError for confidence_level <= 0."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "confidence_level must be between 0 and 1"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        comprehensive_stats(data, confidence_level=0.0)


def test_comprehensive_stats_confidence_level_too_high() -> None:
    """Test case 18: ValueError for confidence_level >= 1."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "confidence_level must be between 0 and 1"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        comprehensive_stats(data, confidence_level=1.0)


def test_comprehensive_stats_invalid_include_distribution_tests_type() -> None:
    """Test case 19: TypeError for invalid include_distribution_tests type."""
    # Arrange
    data = [1, 2, 3]
    expected_message = "include_distribution_tests must be a boolean"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        comprehensive_stats(data, include_distribution_tests="true")


def test_comprehensive_stats_mixed_types() -> None:
    """Test case 20: ValueError for mixed numeric and non-numeric types."""
    # Arrange
    invalid_data = [1, 2, "abc", 4]
    expected_message = "data contains non-numeric values"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        comprehensive_stats(invalid_data)
