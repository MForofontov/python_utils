import pytest
import math
from mathematical_functions.advanced.root_finding import root_finding


def test_root_finding_bisection_linear() -> None:
    """
    Test case 1: Test bisection method with linear function.
    """
    def linear_func(x):
        return 2 * x - 4  # Root at x = 2
    
    result = root_finding(linear_func, (0, 5), method='bisection')
    
    assert abs(result['root'] - 2.0) < 1e-8
    assert result['converged'] == True
    assert result['method_used'] == 'bisection'


def test_root_finding_newton_quadratic() -> None:
    """
    Test case 2: Test Newton-Raphson method with quadratic function.
    """
    def quadratic_func(x):
        return x * x - 4  # Root at x = ±2
    
    def quadratic_derivative(x):
        return 2 * x
    
    result = root_finding(quadratic_func, 1, method='newton', derivative=quadratic_derivative)
    
    assert abs(result['root'] - 2.0) < 1e-8
    assert result['converged'] == True


def test_root_finding_secant_cubic() -> None:
    """
    Test case 3: Test secant method with cubic function.
    """
    def cubic_func(x):
        return x**3 - x - 1  # Root approximately at x ≈ 1.324
    
    result = root_finding(cubic_func, (1, 2), method='secant')
    
    assert abs(cubic_func(result['root'])) < 1e-8
    assert result['converged'] == True


def test_root_finding_false_position() -> None:
    """
    Test case 4: Test false position method.
    """
    def func(x):
        return x * x * x - x - 2  # Root at x = ?
    
    result = root_finding(func, (1, 2), method='false_position')
    
    assert abs(func(result['root'])) < 1e-8
    assert result['converged'] == True


def test_root_finding_brent_method() -> None:
    """
    Test case 5: Test Brent's method.
    """
    def func(x):
        return math.cos(x) - x  # Root approximately at x ≈ 0.739
    
    result = root_finding(func, (0, 1), method='brent')
    
    assert abs(func(result['root'])) < 1e-8
    assert result['converged'] == True


def test_root_finding_illinois_method() -> None:
    """
    Test case 6: Test Illinois method.
    """
    def func(x):
        return x * x - 3  # Root at x = √3 ≈ 1.732
    
    result = root_finding(func, (1, 2), method='illinois')
    
    assert abs(result['root'] - math.sqrt(3)) < 1e-8
    assert result['converged'] == True


def test_root_finding_sine_function() -> None:
    """
    Test case 7: Test root finding with sine function.
    """
    def sine_func(x):
        return math.sin(x)  # Root at x = 0, π, 2π, etc.
    
    result = root_finding(sine_func, (2, 4), method='bisection')
    
    assert abs(result['root'] - math.pi) < 1e-6
    assert result['converged'] == True


def test_root_finding_exponential_function() -> None:
    """
    Test case 8: Test root finding with exponential function.
    """
    def exp_func(x):
        return math.exp(x) - 3  # Root at x = ln(3) ≈ 1.099
    
    result = root_finding(exp_func, (0, 2), method='bisection')
    
    assert abs(result['root'] - math.log(3)) < 1e-6
    assert result['converged'] == True


def test_root_finding_no_root_in_bracket() -> None:
    """
    Test case 9: Test error when no root in bracket for bracketing methods.
    """
    def func(x):
        return x * x + 1  # No real roots
    
    with pytest.raises(ValueError, match="No root in bracket"):
        root_finding(func, (0, 1), method='bisection')


def test_root_finding_invalid_bracket() -> None:
    """
    Test case 10: Test error with invalid bracket.
    """
    def func(x):
        return x
    
    with pytest.raises(ValueError, match="bracket must satisfy a < b"):
        root_finding(func, (2, 1), method='bisection')


def test_root_finding_newton_no_derivative() -> None:
    """
    Test case 11: Test Newton method without derivative.
    """
    def func(x):
        return x * x - 4
    
    # Should use numerical derivative
    result = root_finding(func, 1, method='newton')
    
    assert abs(result['root'] - 2.0) < 1e-6
    assert result['converged'] == True


def test_root_finding_newton_zero_derivative() -> None:
    """
    Test case 12: Test Newton method with zero derivative.
    """
    def func(x):
        return x * x
    
    def zero_derivative(x):
        return 0 if abs(x) < 1e-10 else 2*x
    
    with pytest.raises(ValueError, match="Zero derivative encountered"):
        root_finding(func, 0.0, method='newton', derivative=zero_derivative)


def test_root_finding_invalid_method() -> None:
    """
    Test case 13: Test error with invalid method.
    """
    def func(x):
        return x
    
    with pytest.raises(ValueError, match="method must be one of"):
        root_finding(func, (0, 1), method='invalid_method')


def test_root_finding_type_errors() -> None:
    """
    Test case 14: Test type error handling.
    """
    def func(x):
        return x
    
    with pytest.raises(TypeError, match="func must be callable"):
        root_finding("not a function", (0, 1))
    
    with pytest.raises(TypeError, match="tolerance must be numeric"):
        root_finding(func, (0, 1), tolerance="invalid")
    
    with pytest.raises(TypeError, match="max_iterations must be integer"):
        root_finding(func, (0, 1), max_iterations="invalid")


def test_root_finding_invalid_tolerance() -> None:
    """
    Test case 15: Test invalid tolerance values.
    """
    def func(x):
        return x
    
    with pytest.raises(ValueError, match="tolerance must be positive"):
        root_finding(func, (0, 1), tolerance=0)
    
    with pytest.raises(ValueError, match="tolerance must be positive"):
        root_finding(func, (0, 1), tolerance=-1e-6)


def test_root_finding_invalid_max_iterations() -> None:
    """
    Test case 16: Test invalid max_iterations values.
    """
    def func(x):
        return x
    
    with pytest.raises(ValueError, match="max_iterations must be positive"):
        root_finding(func, (0, 1), max_iterations=0)
    
    with pytest.raises(ValueError, match="max_iterations must be positive"):
        root_finding(func, (0, 1), max_iterations=-10)


def test_root_finding_max_iterations_reached() -> None:
    """
    Test case 17: Test when max iterations is reached.
    """
    def func(x):
        return x * x - 2
    
    result = root_finding(func, (0, 2), method='bisection', max_iterations=5)
    
    assert result['converged'] == False
    assert result['iterations'] == 5


def test_root_finding_function_evaluation_error() -> None:
    """
    Test case 18: Test handling of function evaluation errors.
    """
    def problematic_func(x):
        if abs(x - 0.5) < 1e-10:
            raise ValueError("Function undefined at x=0.5")
        return x - 0.5
    
    with pytest.raises(ValueError, match="Error evaluating function"):
        root_finding(problematic_func, (0, 1), method='bisection')


def test_root_finding_return_structure() -> None:
    """
    Test case 19: Test return structure completeness.
    """
    def func(x):
        return x - 1
    
    result = root_finding(func, (0, 2), method='bisection')
    
    required_keys = ['root', 'function_value', 'iterations', 'converged', 
                    'method_used', 'bracket_history']
    for key in required_keys:
        assert key in result
    
    assert isinstance(result['root'], (int, float))
    assert isinstance(result['iterations'], int)
    assert isinstance(result['converged'], bool)


def test_root_finding_complex_polynomial() -> None:
    """
    Test case 20: Test with higher degree polynomial.
    """
    def poly_func(x):
        return x**4 - 10*x**2 + 9  # (x^2 - 1)(x^2 - 9) = 0, roots at ±1, ±3
    
    result = root_finding(poly_func, (0, 2), method='brent')
    
    assert abs(result['root'] - 1.0) < 1e-8 or abs(result['root'] - 3.0) < 1e-8
    assert result['converged'] == True


def test_root_finding_logarithmic_function() -> None:
    """
    Test case 21: Test with logarithmic function.
    """
    def log_func(x):
        return math.log(x) - 2  # Root at x = e^2
    
    result = root_finding(log_func, (1, 10), method='bisection')
    
    assert abs(result['root'] - math.exp(2)) < 1e-6
    assert result['converged'] == True


def test_root_finding_custom_tolerance() -> None:
    """
    Test case 22: Test with custom tolerance.
    """
    def func(x):
        return x - math.pi
    
    result = root_finding(func, (3, 4), method='bisection', tolerance=1e-12)
    
    assert abs(result['root'] - math.pi) < 1e-10
    assert result['converged'] == True
