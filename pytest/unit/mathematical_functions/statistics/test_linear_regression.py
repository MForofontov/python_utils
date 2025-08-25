import pytest
import numpy as np
from mathematical_functions.statistics.linear_regression import linear_regression


def test_linear_regression_perfect_fit() -> None:
    """
    Test case 1: Test linear regression with perfect linear relationship.
    """
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]  # y = 2x
    
    result = linear_regression(x, y)
    
    assert isinstance(result, dict)
    assert "slope" in result
    assert "intercept" in result
    assert "r_squared" in result
    assert "p_value" in result
    
    assert abs(result["slope"] - 2.0) < 1e-10
    assert abs(result["intercept"] - 0.0) < 1e-10
    assert abs(result["r_squared"] - 1.0) < 1e-10


def test_linear_regression_with_intercept() -> None:
    """
    Test case 2: Test linear regression with non-zero intercept.
    """
    x = [1, 2, 3, 4, 5]
    y = [3, 5, 7, 9, 11]  # y = 2x + 1
    
    result = linear_regression(x, y)
    
    assert abs(result["slope"] - 2.0) < 1e-10
    assert abs(result["intercept"] - 1.0) < 1e-10
    assert abs(result["r_squared"] - 1.0) < 1e-10


def test_linear_regression_negative_slope() -> None:
    """
    Test case 3: Test linear regression with negative slope.
    """
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]  # y = -2x + 12
    
    result = linear_regression(x, y)
    
    assert abs(result["slope"] - (-2.0)) < 1e-10
    assert abs(result["intercept"] - 12.0) < 1e-10
    assert abs(result["r_squared"] - 1.0) < 1e-10


def test_linear_regression_noisy_data() -> None:
    """
    Test case 4: Test linear regression with noisy data.
    """
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2.1, 3.9, 6.2, 7.8, 10.1, 11.9, 14.2, 15.8, 18.1, 20.2]  # y ≈ 2x with noise
    
    result = linear_regression(x, y)
    
    assert 1.8 < result["slope"] < 2.2  # Should be close to 2
    assert -0.5 < result["intercept"] < 0.5  # Should be close to 0
    assert result["r_squared"] > 0.95  # Should have high R²


def test_linear_regression_poor_fit() -> None:
    """
    Test case 5: Test linear regression with poor linear fit.
    """
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 2, 5, 3]  # Random-like pattern
    
    result = linear_regression(x, y)
    
    assert result["r_squared"] < 0.5  # Should have low R²
    assert result["p_value"] > 0.05  # Should not be statistically significant


def test_linear_regression_floating_point() -> None:
    """
    Test case 6: Test linear regression with floating point values.
    """
    x = [1.1, 2.2, 3.3, 4.4, 5.5]
    y = [2.2, 4.4, 6.6, 8.8, 11.0]  # y = 2x
    
    result = linear_regression(x, y)
    
    assert abs(result["slope"] - 2.0) < 1e-10
    assert abs(result["intercept"] - 0.0) < 1e-10


def test_linear_regression_confidence_intervals() -> None:
    """
    Test case 7: Test linear regression includes confidence intervals.
    """
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]  # Perfect fit
    
    result = linear_regression(x, y)
    
    if "slope_ci" in result:
        ci = result["slope_ci"]
        assert len(ci) == 2  # Lower and upper bounds
        assert ci[0] <= result["slope"] <= ci[1]
    
    if "intercept_ci" in result:
        ci = result["intercept_ci"]
        assert len(ci) == 2
        assert ci[0] <= result["intercept"] <= ci[1]


def test_linear_regression_predictions() -> None:
    """
    Test case 8: Test linear regression includes prediction capability.
    """
    x = [1, 2, 3, 4, 5]
    y = [3, 5, 7, 9, 11]  # y = 2x + 1
    
    result = linear_regression(x, y)
    
    # Manual prediction check
    predicted_6 = result["slope"] * 6 + result["intercept"]
    assert abs(predicted_6 - 13.0) < 1e-10  # Should predict 13 for x=6


def test_linear_regression_residuals() -> None:
    """
    Test case 9: Test linear regression includes residual analysis.
    """
    x = [1, 2, 3, 4, 5]
    y = [2.1, 3.9, 6.1, 7.9, 10.1]  # y ≈ 2x with small noise
    
    result = linear_regression(x, y)
    
    if "residuals" in result:
        residuals = result["residuals"]
        assert len(residuals) == len(x)
        # Residuals should sum to approximately zero
        assert abs(sum(residuals)) < 1e-10


def test_linear_regression_larger_dataset() -> None:
    """
    Test case 10: Test linear regression with larger dataset.
    """
    x = list(range(1, 51))  # 1 to 50
    y = [val * 1.5 + 3 for val in x]  # y = 1.5x + 3
    
    result = linear_regression(x, y)
    
    assert abs(result["slope"] - 1.5) < 1e-10
    assert abs(result["intercept"] - 3.0) < 1e-10
    assert result["p_value"] < 0.001  # Should be highly significant


def test_linear_regression_real_world_data() -> None:
    """
    Test case 11: Test linear regression with real-world-like data.
    """
    # Temperature (°F) vs Energy consumption example
    temperature = [20, 30, 40, 50, 60, 70, 80, 90]
    energy = [85, 75, 65, 55, 45, 35, 25, 15]  # Negative correlation
    
    result = linear_regression(temperature, energy)
    
    assert result["slope"] < 0  # Should be negative slope
    assert result["r_squared"] > 0.8  # Should be strong relationship


def test_linear_regression_minimum_data() -> None:
    """
    Test case 12: Test linear regression with minimum data points.
    """
    x = [1, 2]
    y = [3, 4]
    
    result = linear_regression(x, y)
    
    assert result["slope"] == 1.0  # (4-3)/(2-1) = 1
    assert result["intercept"] == 2.0  # y - mx = 3 - 1*1 = 2
    # R² should be 1.0 for perfect fit with 2 points


def test_linear_regression_empty_lists() -> None:
    """
    Test case 13: Test linear regression with empty lists.
    """
    with pytest.raises(ValueError, match="linear regression requires at least 2 values"):
        linear_regression([], [])


def test_linear_regression_single_value() -> None:
    """
    Test case 14: Test linear regression with single value.
    """
    with pytest.raises(ValueError, match="linear regression requires at least 2 values"):
        linear_regression([1], [2])


def test_linear_regression_mismatched_lengths() -> None:
    """
    Test case 15: Test linear regression with mismatched lengths.
    """
    with pytest.raises(ValueError, match="x and y must have the same length"):
        linear_regression([1, 2, 3], [4, 5])


def test_linear_regression_identical_x_values() -> None:
    """
    Test case 16: Test linear regression with identical x values.
    """
    x = [5, 5, 5, 5, 5]
    y = [1, 2, 3, 4, 5]
    
    with pytest.raises(ValueError, match="x values must have variation for regression analysis"):
        linear_regression(x, y)


def test_linear_regression_type_error_not_list() -> None:
    """
    Test case 17: Test linear regression with invalid type for x.
    """
    with pytest.raises(TypeError, match="x must be a list"):
        linear_regression("not a list", [1, 2, 3])


def test_linear_regression_type_error_non_numeric() -> None:
    """
    Test case 18: Test linear regression with non-numeric values.
    """
    with pytest.raises(TypeError, match="all values must be numeric"):
        linear_regression([1, 2, 3], [4, "five", 6])
