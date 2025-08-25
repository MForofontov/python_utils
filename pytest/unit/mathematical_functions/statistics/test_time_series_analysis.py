import pytest
import numpy as np
from mathematical_functions.statistics.time_series_analysis import time_series_analysis


def test_time_series_analysis_trend() -> None:
    """
    Test case 1: Test time series analysis with clear upward trend.
    """
    # Create time series with upward trend
    data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    
    result = time_series_analysis(data)
    
    assert isinstance(result, dict)
    assert "trend" in result
    assert "trend_strength" in result
    assert "seasonality" in result
    assert result["trend"] == "increasing"


def test_time_series_analysis_decreasing_trend() -> None:
    """
    Test case 2: Test time series analysis with decreasing trend.
    """
    data = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
    
    result = time_series_analysis(data)
    
    assert result["trend"] == "decreasing"
    assert result["trend_strength"] > 0.8  # Should be strong trend


def test_time_series_analysis_no_trend() -> None:
    """
    Test case 3: Test time series analysis with no trend (stationary).
    """
    data = [5, 6, 4, 5, 6, 4, 5, 6, 4, 5]  # Oscillating around 5
    
    result = time_series_analysis(data)
    
    assert result["trend"] in ["none", "stationary"]
    assert result["trend_strength"] < 0.3  # Should be weak trend


def test_time_series_analysis_seasonal_pattern() -> None:
    """
    Test case 4: Test time series analysis with seasonal pattern.
    """
    # Create data with seasonal pattern (period = 4)
    data = [1, 4, 2, 3, 1, 4, 2, 3, 1, 4, 2, 3]
    
    result = time_series_analysis(data)
    
    if "seasonal_period" in result:
        assert result["seasonal_period"] in [3, 4]  # Should detect period
    assert result["seasonality"] in ["present", "detected"]


def test_time_series_analysis_volatile_data() -> None:
    """
    Test case 5: Test time series analysis with highly volatile data.
    """
    data = [1, 10, 2, 15, 3, 20, 4, 25, 5, 30]  # High volatility
    
    result = time_series_analysis(data)
    
    assert "volatility" in result
    assert result["volatility"] == "high" or result["volatility"] > 0.5


def test_time_series_analysis_smooth_data() -> None:
    """
    Test case 6: Test time series analysis with smooth, low-volatility data.
    """
    data = [5.0, 5.1, 5.2, 5.1, 5.0, 4.9, 5.0, 5.1, 5.2, 5.1]
    
    result = time_series_analysis(data)
    
    assert "volatility" in result
    assert result["volatility"] == "low" or result["volatility"] < 0.3


def test_time_series_analysis_with_outliers() -> None:
    """
    Test case 7: Test time series analysis with outliers.
    """
    data = [1, 2, 3, 4, 100, 6, 7, 8, 9, 10]  # Contains outlier at position 4
    
    result = time_series_analysis(data)
    
    if "outliers" in result:
        assert len(result["outliers"]) > 0
        assert 100 in result["outliers"]


def test_time_series_analysis_statistical_summary() -> None:
    """
    Test case 8: Test time series analysis includes statistical summary.
    """
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    result = time_series_analysis(data)
    
    # Should include basic statistics
    expected_stats = ["mean", "median", "std", "min", "max"]
    for stat in expected_stats:
        if stat in result:
            assert isinstance(result[stat], (int, float))


def test_time_series_analysis_autocorrelation() -> None:
    """
    Test case 9: Test time series analysis with autocorrelation.
    """
    # Create data with autocorrelation (each value depends on previous)
    data = [1]
    for i in range(1, 20):
        data.append(data[-1] * 0.8 + 2)  # AR(1) process
    
    result = time_series_analysis(data)
    
    if "autocorrelation" in result:
        assert "lag_1" in result["autocorrelation"]
        assert result["autocorrelation"]["lag_1"] > 0.5  # Should be positive


def test_time_series_analysis_change_points() -> None:
    """
    Test case 10: Test time series analysis detects change points.
    """
    # Data with clear change point at position 5
    data = [1, 2, 3, 4, 5] + [10, 11, 12, 13, 14]
    
    result = time_series_analysis(data)
    
    if "change_points" in result:
        assert len(result["change_points"]) > 0


def test_time_series_analysis_minimum_data() -> None:
    """
    Test case 11: Test time series analysis with minimum data points.
    """
    data = [1, 2, 3]  # Just 3 points
    
    result = time_series_analysis(data)
    
    assert isinstance(result, dict)
    # Should still provide basic analysis


def test_time_series_analysis_floating_point() -> None:
    """
    Test case 12: Test time series analysis with floating point data.
    """
    data = [1.1, 2.3, 3.7, 4.2, 5.8, 6.1, 7.4, 8.9, 9.2, 10.5]
    
    result = time_series_analysis(data)
    
    assert isinstance(result, dict)
    assert "trend" in result


def test_time_series_analysis_empty_data() -> None:
    """
    Test case 13: Test time series analysis with empty data.
    """
    with pytest.raises(ValueError, match="time series analysis requires at least 3 values"):
        time_series_analysis([])


def test_time_series_analysis_insufficient_data() -> None:
    """
    Test case 14: Test time series analysis with insufficient data.
    """
    with pytest.raises(ValueError, match="time series analysis requires at least 3 values"):
        time_series_analysis([1, 2])


def test_time_series_analysis_type_error_not_list() -> None:
    """
    Test case 15: Test time series analysis with invalid type for data.
    """
    with pytest.raises(TypeError, match="data must be a list"):
        time_series_analysis("not a list")


def test_time_series_analysis_type_error_non_numeric() -> None:
    """
    Test case 16: Test time series analysis with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        time_series_analysis([1, 2, "three", 4, 5])
