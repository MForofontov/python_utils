import pytest
import math
from mathematical_functions.advanced.polynomial_regression import polynomial_regression


def test_polynomial_regression_linear() -> None:
    """
    Test case 1: Test polynomial regression with degree 1 (linear).
    """
    x_values = [1, 2, 3, 4, 5]
    y_values = [2, 4, 6, 8, 10]  # y = 2x
    degree = 1
    
    coefficients = polynomial_regression(x_values, y_values, degree)
    
    # Should be approximately [0, 2] for y = 0 + 2x
    assert len(coefficients) == 2
    assert abs(coefficients[0]) < 1e-10  # intercept ~0
    assert abs(coefficients[1] - 2.0) < 1e-10  # slope ~2


def test_polynomial_regression_quadratic() -> None:
    """
    Test case 2: Test polynomial regression with degree 2 (quadratic).
    """
    x_values = [1, 2, 3, 4, 5]
    y_values = [1, 4, 9, 16, 25]  # y = x^2
    degree = 2
    
    coefficients = polynomial_regression(x_values, y_values, degree)
    
    # Should be approximately [0, 0, 1] for y = 0 + 0x + 1x^2
    assert len(coefficients) == 3
    assert abs(coefficients[0]) < 1e-10  # constant term ~0
    assert abs(coefficients[1]) < 1e-10  # linear term ~0
    assert abs(coefficients[2] - 1.0) < 1e-10  # quadratic term ~1


def test_polynomial_regression_cubic() -> None:
    """
    Test case 3: Test polynomial regression with degree 3.
    """
    x_values = [1, 2, 3, 4]
    y_values = [1, 8, 27, 64]  # y = x^3
    degree = 3
    
    coefficients = polynomial_regression(x_values, y_values, degree)
    
    # Should be approximately [0, 0, 0, 1] for y = x^3
    assert len(coefficients) == 4
    assert abs(coefficients[3] - 1.0) < 1e-10


def test_polynomial_regression_with_noise() -> None:
    """
    Test case 4: Test polynomial regression with noisy data.
    """
    x_values = [1, 2, 3, 4, 5, 6]
    y_values = [1.1, 3.9, 9.1, 15.9, 25.1, 35.9]  # approximately y = x^2
    degree = 2
    
    coefficients = polynomial_regression(x_values, y_values, degree)
    
    # Should be close to [0, 0, 1] but not exact due to noise
    assert len(coefficients) == 3
    assert abs(coefficients[2] - 1.0) < 0.1  # quadratic term close to 1


def test_polynomial_regression_overdetermined() -> None:
    """
    Test case 5: Test polynomial regression with more data points than degree.
    """
    x_values = [1, 2, 3, 4, 5, 6, 7, 8]
    y_values = [3, 5, 7, 9, 11, 13, 15, 17]  # y = 2x + 1
    degree = 1
    
    coefficients = polynomial_regression(x_values, y_values, degree)
    
    assert len(coefficients) == 2
    assert abs(coefficients[0] - 1.0) < 1e-10  # intercept ~1
    assert abs(coefficients[1] - 2.0) < 1e-10  # slope ~2


def test_polynomial_regression_empty_lists() -> None:
    """
    Test case 6: Test polynomial regression with empty input lists.
    """
    with pytest.raises(ValueError, match="Input lists cannot be empty"):
        polynomial_regression([], [], 1)


def test_polynomial_regression_mismatched_lengths() -> None:
    """
    Test case 7: Test polynomial regression with mismatched list lengths.
    """
    with pytest.raises(ValueError, match="x_values and y_values must have the same length"):
        polynomial_regression([1, 2, 3], [1, 2], 1)


def test_polynomial_regression_insufficient_points() -> None:
    """
    Test case 8: Test polynomial regression with insufficient data points.
    """
    with pytest.raises(ValueError, match="Need at least"):
        polynomial_regression([1, 2], [1, 2], 3)  # degree 3 needs at least 4 points


def test_polynomial_regression_invalid_degree() -> None:
    """
    Test case 9: Test polynomial regression with invalid degree.
    """
    with pytest.raises(ValueError, match="Degree must be non-negative"):
        polynomial_regression([1, 2, 3], [1, 2, 3], -1)


def test_polynomial_regression_type_errors() -> None:
    """
    Test case 10: Test polynomial regression with invalid types.
    """
    with pytest.raises(TypeError, match="x_values must be a list"):
        polynomial_regression("invalid", [1, 2, 3], 1)
    
    with pytest.raises(TypeError, match="y_values must be a list"):
        polynomial_regression([1, 2, 3], "invalid", 1)
    
    with pytest.raises(TypeError, match="degree must be an integer"):
        polynomial_regression([1, 2, 3], [1, 2, 3], "1")


def test_polynomial_regression_non_numeric_values() -> None:
    """
    Test case 11: Test polynomial regression with non-numeric values.
    """
    with pytest.raises(TypeError, match="All values in x_values must be numeric"):
        polynomial_regression([1, "2", 3], [1, 2, 3], 1)
    
    with pytest.raises(TypeError, match="All values in y_values must be numeric"):
        polynomial_regression([1, 2, 3], [1, "2", 3], 1)
