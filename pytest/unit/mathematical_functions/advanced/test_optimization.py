import pytest
import math
from mathematical_functions.advanced.optimization import optimization


def test_optimization_quadratic_minimization() -> None:
    """
    Test case 1: Test quadratic function minimization.
    """
    def quadratic_func(x):
        return (x - 2)**2 + 1  # Minimum at x = 2, f = 1
    
    result = optimization(quadratic_func, (0, 4), method='golden_section')
    
    assert abs(result['x_optimal'] - 2.0) < 1e-6
    assert abs(result['f_optimal'] - 1.0) < 1e-6
    assert result['converged'] == True
    assert result['method_used'] == 'golden_section'


def test_optimization_quadratic_maximization() -> None:
    """
    Test case 2: Test quadratic function maximization.
    """
    def quadratic_func(x):
        return -(x - 3)**2 + 4  # Maximum at x = 3, f = 4
    
    result = optimization(quadratic_func, (1, 5), method='golden_section', maximize=True)
    
    assert abs(result['x_optimal'] - 3.0) < 1e-6
    assert abs(result['f_optimal'] - 4.0) < 1e-6
    assert result['converged'] == True


def test_optimization_ternary_search() -> None:
    """
    Test case 3: Test ternary search method.
    """
    def func(x):
        return x**2 - 4*x + 3  # Minimum at x = 2, f = -1
    
    result = optimization(func, (0, 4), method='ternary_search')
    
    assert abs(result['x_optimal'] - 2.0) < 1e-6
    assert abs(result['f_optimal'] - (-1.0)) < 1e-6


def test_optimization_brent_method() -> None:
    """
    Test case 4: Test Brent's method.
    """
    def func(x):
        return x**4 - 14*x**3 + 60*x**2 - 70*x  # Complex function
    
    result = optimization(func, (0, 2), method='brent')
    
    assert result['converged'] == True
    assert isinstance(result['x_optimal'], (int, float))
    assert isinstance(result['f_optimal'], (int, float))


def test_optimization_fibonacci_search() -> None:
    """
    Test case 5: Test Fibonacci search method.
    """
    def func(x):
        return x**2 + 2*x + 1  # (x + 1)^2, minimum at x = -1
    
    result = optimization(func, (-3, 1), method='fibonacci')
    
    assert abs(result['x_optimal'] - (-1.0)) < 1e-4
    assert abs(result['f_optimal']) < 1e-6


def test_optimization_parabolic_interpolation() -> None:
    """
    Test case 6: Test parabolic interpolation method.
    """
    def func(x):
        return x**2 - 6*x + 9  # (x - 3)^2, minimum at x = 3
    
    result = optimization(func, (1, 5), method='parabolic')
    
    assert abs(result['x_optimal'] - 3.0) < 1e-4
    assert abs(result['f_optimal']) < 1e-6


def test_optimization_grid_search() -> None:
    """
    Test case 7: Test grid search method.
    """
    def func(x):
        return (x - 1.5)**2 + 0.5  # Minimum at x = 1.5
    
    result = optimization(func, (0, 3), method='grid_search', n_points=50)
    
    assert abs(result['x_optimal'] - 1.5) < 0.1
    assert result['converged'] == True


def test_optimization_sine_function() -> None:
    """
    Test case 8: Test optimization of sine function.
    """
    def sine_func(x):
        return math.sin(x)  # Minimum at -π/2, maximum at π/2
    
    result = optimization(sine_func, (-2, 2), method='golden_section')
    
    # Should find minimum around -π/2
    assert abs(result['f_optimal'] - (-1.0)) < 1e-6


def test_optimization_exponential_function() -> None:
    """
    Test case 9: Test optimization of exponential function.
    """
    def exp_func(x):
        return math.exp(x - 2)  # Monotonically increasing
    
    result = optimization(exp_func, (0, 4), method='golden_section')
    
    # Should find minimum at left boundary
    assert abs(result['x_optimal'] - 0.0) < 1e-6


def test_optimization_custom_tolerance() -> None:
    """
    Test case 10: Test optimization with custom tolerance.
    """
    def func(x):
        return (x - math.pi)**2
    
    result = optimization(func, (2, 4), method='golden_section', tolerance=1e-12)
    
    assert abs(result['x_optimal'] - math.pi) < 1e-10
    assert result['converged'] == True


def test_optimization_max_iterations() -> None:
    """
    Test case 11: Test optimization with limited iterations.
    """
    def func(x):
        return x**2 - 4*x + 4
    
    result = optimization(func, (0, 4), method='golden_section', max_iterations=5)
    
    # Should reach max iterations
    assert result['iterations'] <= 5


def test_optimization_invalid_bounds() -> None:
    """
    Test case 12: Test error with invalid bounds.
    """
    def func(x):
        return x**2
    
    with pytest.raises(ValueError, match="bounds must satisfy a < b"):
        optimization(func, (2, 1), method='golden_section')


def test_optimization_invalid_function() -> None:
    """
    Test case 13: Test error with invalid function.
    """
    with pytest.raises(TypeError, match="func must be callable"):
        optimization("not a function", (0, 1), method='golden_section')


def test_optimization_invalid_method() -> None:
    """
    Test case 14: Test error with invalid method.
    """
    def func(x):
        return x**2
    
    with pytest.raises(ValueError, match="method must be one of"):
        optimization(func, (0, 1), method='invalid_method')


def test_optimization_type_errors() -> None:
    """
    Test case 15: Test type error handling.
    """
    def func(x):
        return x**2
    
    with pytest.raises(TypeError, match="bounds must be a tuple"):
        optimization(func, "invalid", method='golden_section')
    
    with pytest.raises(TypeError, match="bounds must contain numeric values"):
        optimization(func, ("0", "1"), method='golden_section')
    
    with pytest.raises(ValueError, match="tolerance must be positive"):
        optimization(func, (0, 1), method='golden_section', tolerance=0)
    
    with pytest.raises(ValueError, match="max_iterations must be positive integer"):
        optimization(func, (0, 1), method='golden_section', max_iterations=0)


def test_optimization_polynomial_function() -> None:
    """
    Test case 16: Test optimization of higher-degree polynomial.
    """
    def poly_func(x):
        return x**4 - 4*x**3 + 6*x**2 - 4*x + 1  # (x - 1)^4
    
    result = optimization(poly_func, (0, 2), method='brent')
    
    assert abs(result['x_optimal'] - 1.0) < 1e-6
    assert abs(result['f_optimal']) < 1e-10


def test_optimization_logarithmic_function() -> None:
    """
    Test case 17: Test optimization of logarithmic function.
    """
    def log_func(x):
        return x * math.log(x)  # Minimum at x = 1/e
    
    result = optimization(log_func, (0.1, 1), method='golden_section')
    
    expected_x = 1 / math.e
    assert abs(result['x_optimal'] - expected_x) < 1e-4


def test_optimization_grid_search_parameters() -> None:
    """
    Test case 18: Test grid search with different parameters.
    """
    def func(x):
        return x**2 - 2*x + 1
    
    result = optimization(func, (0, 2), method='grid_search', 
                         n_points=20, refinement_levels=2)
    
    assert abs(result['x_optimal'] - 1.0) < 0.2
    assert result['converged'] == True


def test_optimization_return_structure() -> None:
    """
    Test case 19: Test return structure completeness.
    """
    def func(x):
        return x**2
    
    result = optimization(func, (-1, 1), method='golden_section')
    
    required_keys = ['x_optimal', 'f_optimal', 'iterations', 'converged',
                    'method_used', 'function_evaluations', 'final_interval']
    for key in required_keys:
        assert key in result
    
    assert isinstance(result['x_optimal'], (int, float))
    assert isinstance(result['f_optimal'], (int, float))
    assert isinstance(result['iterations'], int)
    assert isinstance(result['converged'], bool)
    assert isinstance(result['function_evaluations'], int)


def test_optimization_function_evaluation_count() -> None:
    """
    Test case 20: Test function evaluation counting.
    """
    evaluation_count = 0
    
    def counting_func(x):
        nonlocal evaluation_count
        evaluation_count += 1
        return x**2
    
    result = optimization(counting_func, (0, 2), method='golden_section')
    
    # Function evaluation count should match
    assert result['function_evaluations'] >= evaluation_count
    assert result['function_evaluations'] > 0


def test_optimization_cosine_function() -> None:
    """
    Test case 21: Test optimization of cosine function.
    """
    def cos_func(x):
        return -math.cos(x)  # Maximum of cos(x) = minimum of -cos(x)
    
    result = optimization(cos_func, (-1, 1), method='golden_section')
    
    # Should find minimum around x = 0 (where cos is maximum)
    assert abs(result['x_optimal']) < 0.1
    assert abs(result['f_optimal'] - (-1.0)) < 1e-6


def test_optimization_boundary_minimum() -> None:
    """
    Test case 22: Test when minimum is at boundary.
    """
    def linear_func(x):
        return 2*x + 1  # Monotonically increasing
    
    result = optimization(linear_func, (0, 3), method='golden_section')
    
    # Should find minimum at left boundary
    assert abs(result['x_optimal'] - 0.0) < 1e-6
    assert abs(result['f_optimal'] - 1.0) < 1e-6
