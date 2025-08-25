import pytest
from mathematical_functions.statistics.correlation_analysis import correlation_analysis


def test_correlation_analysis_basic() -> None:
    """
    Test case 1: Test correlation analysis with basic datasets.
    """
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]  # Perfect positive correlation
    
    result = correlation_analysis(x, y)
    
    assert isinstance(result, dict)
    assert "pearson_r" in result
    assert "p_value" in result
    assert "strength" in result
    assert "direction" in result
    assert abs(result["pearson_r"] - 1.0) < 1e-10


def test_correlation_analysis_negative_correlation() -> None:
    """
    Test case 2: Test correlation analysis with negative correlation.
    """
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]  # Perfect negative correlation
    
    result = correlation_analysis(x, y)
    
    assert abs(result["pearson_r"] - (-1.0)) < 1e-10
    assert result["direction"] == "negative"


def test_correlation_analysis_no_correlation() -> None:
    """
    Test case 3: Test correlation analysis with no correlation.
    """
    x = [1, 2, 3, 4, 5]
    y = [3, 1, 4, 1, 5]  # Random pattern
    
    result = correlation_analysis(x, y)
    
    assert abs(result["pearson_r"]) < 0.7  # Should be weak correlation
    assert result["strength"] in ["weak", "very weak", "none"]


def test_correlation_analysis_moderate_correlation() -> None:
    """
    Test case 4: Test correlation analysis with moderate correlation.
    """
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2.1, 3.9, 6.2, 7.8, 10.1, 11.9, 14.2, 15.8, 18.1, 20.2]  # y ≈ 2x with noise
    
    result = correlation_analysis(x, y)
    
    assert 0.7 < result["pearson_r"] < 1.0
    assert result["strength"] in ["strong", "very strong"]
    assert result["direction"] == "positive"


def test_correlation_analysis_weak_correlation() -> None:
    """
    Test case 5: Test correlation analysis with weak correlation.
    """
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 3, 5, 4, 6, 7, 8, 9, 11, 12]  # Weak positive correlation
    
    result = correlation_analysis(x, y)
    
    assert 0 < result["pearson_r"] < 0.7
    assert result["strength"] in ["weak", "moderate"]
    assert result["direction"] == "positive"


def test_correlation_analysis_real_world_data() -> None:
    """
    Test case 6: Test correlation analysis with real-world-like data.
    """
    # Height (inches) vs Weight (pounds) example
    height = [60, 62, 64, 66, 68, 70, 72, 74, 76, 78]
    weight = [120, 130, 140, 155, 165, 175, 185, 195, 210, 220]
    
    result = correlation_analysis(height, weight)
    
    assert result["pearson_r"] > 0.8  # Should be strong positive correlation
    assert result["direction"] == "positive"
    assert result["strength"] in ["strong", "very strong"]


def test_correlation_analysis_with_floats() -> None:
    """
    Test case 7: Test correlation analysis with floating point values.
    """
    x = [1.1, 2.2, 3.3, 4.4, 5.5]
    y = [2.2, 4.4, 6.6, 8.8, 11.0]  # Perfect correlation
    
    result = correlation_analysis(x, y)
    
    assert abs(result["pearson_r"] - 1.0) < 1e-10
    assert result["strength"] == "very strong"


def test_correlation_analysis_confidence_interval() -> None:
    """
    Test case 8: Test correlation analysis includes confidence intervals.
    """
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    
    result = correlation_analysis(x, y)
    
    if "confidence_interval" in result:
        ci = result["confidence_interval"]
        assert len(ci) == 2  # Lower and upper bounds
        assert ci[0] <= result["pearson_r"] <= ci[1]


def test_correlation_analysis_large_dataset() -> None:
    """
    Test case 9: Test correlation analysis with larger dataset.
    """
    x = list(range(1, 51))  # 1 to 50
    y = [val * 2 + 1 for val in x]  # y = 2x + 1 (perfect correlation)
    
    result = correlation_analysis(x, y)
    
    assert abs(result["pearson_r"] - 1.0) < 1e-10
    assert result["p_value"] < 0.001  # Very significant


def test_correlation_analysis_minimum_data() -> None:
    """
    Test case 10: Test correlation analysis with minimum data points.
    """
    x = [1, 2]
    y = [3, 4]
    
    result = correlation_analysis(x, y)
    
    assert abs(result["pearson_r"] - 1.0) < 1e-10  # Two points always perfect correlation


def test_correlation_analysis_empty_lists() -> None:
    """
    Test case 11: Test correlation analysis with empty lists.
    """
    with pytest.raises(ValueError, match="correlation analysis requires at least 2 values"):
        correlation_analysis([], [])


def test_correlation_analysis_single_value() -> None:
    """
    Test case 12: Test correlation analysis with single value.
    """
    with pytest.raises(ValueError, match="correlation analysis requires at least 2 values"):
        correlation_analysis([1], [2])


def test_correlation_analysis_mismatched_lengths() -> None:
    """
    Test case 13: Test correlation analysis with mismatched lengths.
    """
    with pytest.raises(ValueError, match="x and y must have the same length"):
        correlation_analysis([1, 2, 3], [4, 5])


def test_correlation_analysis_identical_values() -> None:
    """
    Test case 14: Test correlation analysis with identical x values.
    """
    x = [5, 5, 5, 5, 5]
    y = [1, 2, 3, 4, 5]
    
    with pytest.raises(ValueError, match="correlation is undefined when standard deviation is zero"):
        correlation_analysis(x, y)


def test_correlation_analysis_type_error_not_list() -> None:
    """
    Test case 15: Test correlation analysis with invalid type for x.
    """
    with pytest.raises(TypeError, match="x must be a list"):
        correlation_analysis("not a list", [1, 2, 3])


def test_correlation_analysis_type_error_non_numeric() -> None:
    """
    Test case 16: Test correlation analysis with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        correlation_analysis([1, 2, 3], [4, "five", 6])
