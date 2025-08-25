import pytest
import math
from mathematical_functions.advanced.numerical_integration import numerical_integration


def test_numerical_integration_linear_function() -> None:
    """
    Test case 1: Test numerical integration of a linear function.
    """
    def linear_func(x):
        return 2 * x + 1
    
    # Integral of 2x + 1 from 0 to 2 is [x^2 + x] = 4 + 2 = 6
    result = numerical_integration(linear_func, 0, 2, 1000)
    assert abs(result - 6.0) < 0.01


def test_numerical_integration_quadratic_function() -> None:
    """
    Test case 2: Test numerical integration of a quadratic function.
    """
    def quadratic_func(x):
        return x * x
    
    # Integral of x^2 from 0 to 3 is [x^3/3] = 27/3 = 9
    result = numerical_integration(quadratic_func, 0, 3, 1000)
    assert abs(result - 9.0) < 0.01


def test_numerical_integration_sine_function() -> None:
    """
    Test case 3: Test numerical integration of sine function.
    """
    def sine_func(x):
        return math.sin(x)
    
    # Integral of sin(x) from 0 to pi is [-cos(x)] = -(-1) - (-1) = 2
    result = numerical_integration(sine_func, 0, math.pi, 1000)
    assert abs(result - 2.0) < 0.01


def test_numerical_integration_exponential_function() -> None:
    """
    Test case 4: Test numerical integration of exponential function.
    """
    def exp_func(x):
        return math.exp(x)
    
    # Integral of e^x from 0 to 1 is [e^x] = e - 1 ≈ 1.718
    result = numerical_integration(exp_func, 0, 1, 1000)
    expected = math.e - 1
    assert abs(result - expected) < 0.01


def test_numerical_integration_constant_function() -> None:
    """
    Test case 5: Test numerical integration of a constant function.
    """
    def constant_func(x):
        return 5
    
    # Integral of 5 from 1 to 4 is 5 * (4 - 1) = 15
    result = numerical_integration(constant_func, 1, 4, 100)
    assert abs(result - 15.0) < 0.01


def test_numerical_integration_negative_interval() -> None:
    """
    Test case 6: Test numerical integration with negative interval.
    """
    def linear_func(x):
        return x
    
    # Integral of x from -2 to 2 is [x^2/2] = 2 - 2 = 0
    result = numerical_integration(linear_func, -2, 2, 1000)
    assert abs(result - 0.0) < 0.01


def test_numerical_integration_reversed_bounds() -> None:
    """
    Test case 7: Test numerical integration with reversed bounds.
    """
    def quadratic_func(x):
        return x * x
    
    # Integral from 3 to 0 should be negative of integral from 0 to 3
    result = numerical_integration(quadratic_func, 3, 0, 1000)
    expected = numerical_integration(quadratic_func, 0, 3, 1000)
    assert abs(result + expected) < 0.01


def test_numerical_integration_complex_function() -> None:
    """
    Test case 8: Test numerical integration of a complex function.
    """
    def complex_func(x):
        return x**3 - 2*x**2 + x + 1
    
    # This should work with any reasonable result
    result = numerical_integration(complex_func, 0, 2, 1000)
    assert isinstance(result, float)


def test_numerical_integration_invalid_function() -> None:
    """
    Test case 9: Test numerical integration with invalid function.
    """
    with pytest.raises(TypeError, match="func must be callable"):
        numerical_integration("not a function", 0, 1, 100)


def test_numerical_integration_invalid_bounds() -> None:
    """
    Test case 10: Test numerical integration with invalid bounds.
    """
    def simple_func(x):
        return x
    
    with pytest.raises(TypeError, match="a must be numeric"):
        numerical_integration(simple_func, "0", 1, 100)
    
    with pytest.raises(TypeError, match="b must be numeric"):
        numerical_integration(simple_func, 0, "1", 100)


def test_numerical_integration_invalid_n() -> None:
    """
    Test case 11: Test numerical integration with invalid n.
    """
    def simple_func(x):
        return x
    
    with pytest.raises(TypeError, match="n must be an integer"):
        numerical_integration(simple_func, 0, 1, "100")
    
    with pytest.raises(ValueError, match="n must be positive"):
        numerical_integration(simple_func, 0, 1, 0)
    
    with pytest.raises(ValueError, match="n must be positive"):
        numerical_integration(simple_func, 0, 1, -10)


def test_numerical_integration_function_error() -> None:
    """
    Test case 12: Test numerical integration when function raises error.
    """
    def problematic_func(x):
        if x == 0.5:
            raise ValueError("Function error at x=0.5")
        return x
    
    with pytest.raises(ValueError, match="Error evaluating function"):
        numerical_integration(problematic_func, 0, 1, 100)
