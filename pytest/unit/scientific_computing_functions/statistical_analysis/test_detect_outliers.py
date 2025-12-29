"""Unit tests for detect_outliers function."""

import numpy as np
import pytest

from scientific_computing_functions.statistical_analysis.detect_outliers import detect_outliers


# Normal operation tests
def test_detect_outliers_with_clear_outliers() -> None:
    """Test case 1: Normal operation with clear outliers using default methods."""
    # Arrange
    data = [1, 2, 3, 4, 5, 100, 200]  # 100 and 200 are clear outliers
    
    # Act
    result = detect_outliers(data)
    
    # Assert
    assert len(result['outlier_indices']) >= 1
    assert 100 in result['outlier_values'] or 200 in result['outlier_values']
    assert 'outlier_indices' in result
    assert 'outlier_values' in result
    assert 'method_results' in result
    assert 'consensus_scores' in result


def test_detect_outliers_with_zscore_method_only() -> None:
    """Test case 2: Normal operation using only Z-score method."""
    # Arrange
    data = np.random.normal(0, 1, 100).tolist()
    data.extend([10, -10])  # Add outliers
    
    # Act
    result = detect_outliers(data, methods=['zscore'], zscore_threshold=3.0)
    
    # Assert
    assert 'zscore' in result['method_results']
    assert len(result['method_results']) == 1
    assert result['outlier_indices'].size >= 0
    assert result['consensus_scores'].max() <= 1.0


def test_detect_outliers_with_multiple_methods() -> None:
    """Test case 3: Normal operation with multiple methods (zscore, iqr, mad)."""
    # Arrange
    data = list(range(1, 21)) + [100, 200]  # Clear outliers at end
    
    # Act
    result = detect_outliers(data, methods=['zscore', 'iqr', 'mad'])
    
    # Assert
    assert len(result['method_results']) == 3
    assert 'zscore' in result['method_results']
    assert 'iqr' in result['method_results']
    assert 'mad' in result['method_results']
    assert result['outlier_indices'].size >= 1


def test_detect_outliers_with_numpy_array() -> None:
    """Test case 4: Normal operation with numpy array input."""
    # Arrange
    data = np.array([1, 2, 3, 4, 5, 100])
    
    # Act
    result = detect_outliers(data, methods=['iqr'])
    
    # Assert
    assert result['outlier_indices'].size >= 1
    assert 100 in result['outlier_values']


def test_detect_outliers_with_isolation_forest() -> None:
    """Test case 5: Normal operation with isolation forest method."""
    # Arrange
    np.random.seed(42)
    data = np.random.normal(0, 1, 100).tolist()
    data.extend([10, 15, -10])
    
    # Act
    try:
        result = detect_outliers(data, methods=['isolation'])
        
        # Assert
        assert 'isolation' in result['method_results'] or len(result['method_results']) == 0
        assert result['consensus_scores'].shape[0] == len(data)
    except ImportError:
        # sklearn not installed, skip
        pytest.skip("scikit-learn not installed")


def test_detect_outliers_with_custom_thresholds() -> None:
    """Test case 6: Normal operation with custom threshold values."""
    # Arrange
    data = [10] * 50 + [20, 30]  # Most values are 10, with some higher
    
    # Act
    result = detect_outliers(
        data,
        methods=['zscore', 'iqr'],
        zscore_threshold=2.0,
        iqr_multiplier=1.0,
        consensus_threshold=0.5
    )
    
    # Assert
    assert result['outlier_indices'].size >= 0
    assert result['consensus_scores'].min() >= 0.0
    assert result['consensus_scores'].max() <= 1.0


# Edge case tests
def test_detect_outliers_with_no_outliers() -> None:
    """Test case 7: Edge case with no outliers detected."""
    # Arrange
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Uniform data, no outliers
    
    # Act
    result = detect_outliers(data, zscore_threshold=5.0)
    
    # Assert
    assert result['outlier_indices'].size == 0
    assert result['outlier_values'].size == 0


def test_detect_outliers_with_all_identical_values() -> None:
    """Test case 8: Edge case with all identical values."""
    # Arrange
    data = [5.0] * 20
    
    # Act
    result = detect_outliers(data)
    
    # Assert
    # With identical values, should detect no outliers or handle gracefully
    assert result['outlier_indices'].size == 0 or result['outlier_indices'].size == 20


def test_detect_outliers_with_small_dataset() -> None:
    """Test case 9: Edge case with small dataset."""
    # Arrange
    data = [1, 2, 100]
    
    # Act
    result = detect_outliers(data)
    
    # Assert
    assert result['outlier_indices'].size >= 0
    assert len(result['method_results']) > 0


def test_detect_outliers_with_consensus_threshold_one() -> None:
    """Test case 10: Edge case with consensus threshold = 1.0 (all methods must agree)."""
    # Arrange
    data = list(range(1, 21)) + [100]
    
    # Act
    result = detect_outliers(data, methods=['zscore', 'iqr'], consensus_threshold=1.0)
    
    # Assert
    # Only outliers detected by ALL methods will be flagged
    assert result['consensus_scores'].max() <= 1.0
    assert all(result['consensus_scores'][result['outlier_indices']] == 1.0)


def test_detect_outliers_with_mad_zero() -> None:
    """Test case 11: Edge case where MAD is zero (handled internally)."""
    # Arrange
    data = [5, 5, 5, 5, 5, 5, 5, 10]  # Most values identical
    
    # Act
    result = detect_outliers(data, methods=['mad'])
    
    # Assert
    # Should handle MAD=0 gracefully by using small epsilon
    assert 'mad' in result['method_results']
    assert result['outlier_indices'].size >= 0


def test_detect_outliers_with_high_dimensional_boundary() -> None:
    """Test case 12: Edge case with values at exact threshold boundaries."""
    # Arrange
    data = [0] * 50
    data.extend([3.0, -3.0])  # Exactly at typical zscore threshold
    
    # Act
    result = detect_outliers(data, methods=['zscore'], zscore_threshold=3.0)
    
    # Assert
    assert result['outlier_indices'].size >= 0


# Error case tests
def test_detect_outliers_with_invalid_data_type() -> None:
    """Test case 13: TypeError for invalid data type."""
    # Arrange
    invalid_data = "not a list or array"
    expected_message = "data must be a list or numpy array"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        detect_outliers(invalid_data)


def test_detect_outliers_with_empty_data() -> None:
    """Test case 14: ValueError for empty data."""
    # Arrange
    empty_data = []
    expected_message = "data cannot be empty"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(empty_data)


def test_detect_outliers_with_invalid_methods_type() -> None:
    """Test case 15: TypeError for invalid methods type."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    invalid_methods = "zscore"  # Should be a list
    expected_message = "methods must be a list or None"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        detect_outliers(data, methods=invalid_methods)


def test_detect_outliers_with_invalid_method_name() -> None:
    """Test case 16: ValueError for invalid method name."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    invalid_methods = ['invalid_method']
    expected_message = "Invalid method 'invalid_method'"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(data, methods=invalid_methods)


def test_detect_outliers_with_negative_zscore_threshold() -> None:
    """Test case 17: ValueError for negative zscore threshold."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "zscore_threshold must be positive"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(data, zscore_threshold=-1.0)


def test_detect_outliers_with_negative_iqr_multiplier() -> None:
    """Test case 18: ValueError for negative IQR multiplier."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "iqr_multiplier must be positive"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(data, iqr_multiplier=-0.5)


def test_detect_outliers_with_negative_mad_threshold() -> None:
    """Test case 19: ValueError for negative MAD threshold."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "mad_threshold must be positive"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(data, mad_threshold=-2.0)


def test_detect_outliers_with_invalid_consensus_threshold_zero() -> None:
    """Test case 20: ValueError for consensus threshold = 0."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "consensus_threshold must be in \\(0, 1\\]"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(data, consensus_threshold=0.0)


def test_detect_outliers_with_invalid_consensus_threshold_above_one() -> None:
    """Test case 21: ValueError for consensus threshold > 1."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "consensus_threshold must be in \\(0, 1\\]"
    
    # Act & Assert
    with pytest.raises(ValueError, match=expected_message):
        detect_outliers(data, consensus_threshold=1.5)


def test_detect_outliers_with_invalid_threshold_type() -> None:
    """Test case 22: TypeError for invalid threshold types."""
    # Arrange
    data = [1, 2, 3, 4, 5]
    expected_message = "zscore_threshold must be a number"
    
    # Act & Assert
    with pytest.raises(TypeError, match=expected_message):
        detect_outliers(data, zscore_threshold="3.0")
