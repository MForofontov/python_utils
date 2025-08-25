import pytest
from mathematical_functions.statistics.outlier_detection import outlier_detection


def test_outlier_detection_iqr_method() -> None:
    """
    Test case 1: Test outlier detection using IQR method.
    """
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]  # 100 is clearly an outlier
    
    outliers, cleaned_data = outlier_detection(data, method='iqr')
    
    assert 100 in outliers
    assert 100 not in cleaned_data
    assert len(cleaned_data) == len(data) - 1


def test_outlier_detection_zscore_method() -> None:
    """
    Test case 2: Test outlier detection using Z-score method.
    """
    data = [10, 12, 14, 13, 11, 15, 12, 14, 13, 50]  # 50 is an outlier
    
    outliers, cleaned_data = outlier_detection(data, method='zscore', threshold=2.0)
    
    assert 50 in outliers
    assert 50 not in cleaned_data


def test_outlier_detection_modified_zscore() -> None:
    """
    Test case 3: Test outlier detection using modified Z-score method.
    """
    data = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 100]  # 100 is an outlier
    
    outliers, cleaned_data = outlier_detection(data, method='modified_zscore', threshold=3.5)
    
    assert 100 in outliers
    assert 100 not in cleaned_data


def test_outlier_detection_no_outliers() -> None:
    """
    Test case 4: Test outlier detection with no outliers.
    """
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Normal distribution, no outliers
    
    outliers, cleaned_data = outlier_detection(data, method='iqr')
    
    assert len(outliers) == 0
    assert len(cleaned_data) == len(data)
    assert cleaned_data == data


def test_outlier_detection_multiple_outliers() -> None:
    """
    Test case 5: Test outlier detection with multiple outliers.
    """
    data = [-50, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 200]  # Multiple outliers
    
    outliers, cleaned_data = outlier_detection(data, method='iqr')
    
    assert len(outliers) >= 2  # Should detect multiple outliers
    assert -50 in outliers or 100 in outliers or 200 in outliers


def test_outlier_detection_identical_values() -> None:
    """
    Test case 6: Test outlier detection with identical values.
    """
    data = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]  # All identical
    
    outliers, cleaned_data = outlier_detection(data, method='iqr')
    
    assert len(outliers) == 0
    assert cleaned_data == data


def test_outlier_detection_small_dataset() -> None:
    """
    Test case 7: Test outlier detection with small dataset.
    """
    data = [1, 2, 100]  # Very small dataset
    
    outliers, cleaned_data = outlier_detection(data, method='iqr')
    
    # Should still work with small datasets
    assert isinstance(outliers, list)
    assert isinstance(cleaned_data, list)


def test_outlier_detection_negative_values() -> None:
    """
    Test case 8: Test outlier detection with negative values.
    """
    data = [-10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10, -100]  # -100 is outlier
    
    outliers, cleaned_data = outlier_detection(data, method='zscore', threshold=2.0)
    
    assert -100 in outliers
    assert -100 not in cleaned_data


def test_outlier_detection_empty_data() -> None:
    """
    Test case 9: Test outlier detection with empty data.
    """
    with pytest.raises(ValueError, match="Data cannot be empty"):
        outlier_detection([], method='iqr')


def test_outlier_detection_invalid_method() -> None:
    """
    Test case 10: Test outlier detection with invalid method.
    """
    data = [1, 2, 3, 4, 5]
    
    with pytest.raises(ValueError, match="Invalid method"):
        outlier_detection(data, method='invalid_method')


def test_outlier_detection_invalid_type() -> None:
    """
    Test case 11: Test outlier detection with invalid data type.
    """
    with pytest.raises(TypeError, match="data must be a list"):
        outlier_detection("invalid", method='iqr')


def test_outlier_detection_non_numeric() -> None:
    """
    Test case 12: Test outlier detection with non-numeric values.
    """
    with pytest.raises(TypeError, match="All values must be numeric"):
        outlier_detection([1, 2, "3", 4, 5], method='iqr')


def test_outlier_detection_invalid_threshold() -> None:
    """
    Test case 13: Test outlier detection with invalid threshold.
    """
    data = [1, 2, 3, 4, 5]
    
    with pytest.raises(TypeError, match="threshold must be numeric"):
        outlier_detection(data, method='zscore', threshold="invalid")
    
    with pytest.raises(ValueError, match="threshold must be positive"):
        outlier_detection(data, method='zscore', threshold=-1.0)


def test_outlier_detection_single_value() -> None:
    """
    Test case 14: Test outlier detection with single value.
    """
    data = [42]
    
    outliers, cleaned_data = outlier_detection(data, method='iqr')
    
    # Single value cannot be an outlier
    assert len(outliers) == 0
    assert cleaned_data == data
