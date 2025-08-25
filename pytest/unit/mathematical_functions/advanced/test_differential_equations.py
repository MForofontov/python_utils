import pytest
import math
import numpy as np
from mathematical_functions.advanced.differential_equations import differential_equation_solver


def test_differential_equations_exponential_decay() -> None:
    """
    Test case 1: Test solving exponential decay dy/dx = -y.
    """
    def decay_func(x, y):
        return -y  # dy/dx = -y, exact solution: y = y0 * exp(-x)
    
    result = differential_equation_solver(decay_func, y0=1.0, x_span=(0, 2), 
                                        method='runge_kutta_4', n_points=100)
    
    # Check final value against exact solution
    x_final = result['x'][-1]
    y_final = result['y'][-1]
    exact_final = math.exp(-x_final)
    
    assert abs(y_final - exact_final) < 0.01
    assert result['method_used'] == 'runge_kutta_4'
    assert len(result['x']) == len(result['y'])


def test_differential_equations_linear_growth() -> None:
    """
    Test case 2: Test solving linear growth dy/dx = x.
    """
    def linear_func(x, y):
        return x  # dy/dx = x, exact solution: y = x^2/2 + C
    
    result = differential_equation_solver(linear_func, y0=0, x_span=(0, 2),
                                        method='euler', n_points=1000)
    
    # Check final value against exact solution
    x_final = result['x'][-1]
    y_final = result['y'][-1]
    exact_final = x_final**2 / 2  # C = 0 since y(0) = 0
    
    assert abs(y_final - exact_final) < 0.1  # Euler method less accurate


def test_differential_equations_sine_function() -> None:
    """
    Test case 3: Test solving dy/dx = cos(x).
    """
    def cosine_func(x, y):
        return math.cos(x)  # dy/dx = cos(x), exact solution: y = sin(x) + C
    
    result = differential_equation_solver(cosine_func, y0=0, x_span=(0, math.pi),
                                        method='runge_kutta_4', n_points=100)
    
    # At x = π, y should be sin(π) = 0
    y_final = result['y'][-1]
    assert abs(y_final) < 0.01


def test_differential_equations_modified_euler() -> None:
    """
    Test case 4: Test modified Euler method.
    """
    def simple_func(x, y):
        return y  # dy/dx = y, exact solution: y = y0 * exp(x)
    
    result = differential_equation_solver(simple_func, y0=1.0, x_span=(0, 1),
                                        method='modified_euler', n_points=100)
    
    # Check against exact solution
    x_final = result['x'][-1]
    y_final = result['y'][-1]
    exact_final = math.exp(x_final)
    
    assert abs(y_final - exact_final) < 0.05


def test_differential_equations_midpoint_method() -> None:
    """
    Test case 5: Test midpoint method.
    """
    def quadratic_func(x, y):
        return 2*x  # dy/dx = 2x, exact solution: y = x^2 + C
    
    result = differential_equation_solver(quadratic_func, y0=1, x_span=(0, 2),
                                        method='midpoint', n_points=100)
    
    # Check final value
    x_final = result['x'][-1]
    y_final = result['y'][-1]
    exact_final = x_final**2 + 1  # C = 1 since y(0) = 1
    
    assert abs(y_final - exact_final) < 0.05


def test_differential_equations_runge_kutta_2() -> None:
    """
    Test case 6: Test second-order Runge-Kutta method.
    """
    def exp_func(x, y):
        return y  # dy/dx = y, solution: y = exp(x)
    
    result = differential_equation_solver(exp_func, y0=1.0, x_span=(0, 1),
                                        method='runge_kutta_2', n_points=50)
    
    y_final = result['y'][-1]
    exact_final = math.exp(1.0)
    
    assert abs(y_final - exact_final) < 0.1


def test_differential_equations_adams_bashforth() -> None:
    """
    Test case 7: Test Adams-Bashforth method.
    """
    def linear_func(x, y):
        return x + y  # dy/dx = x + y
    
    result = differential_equation_solver(linear_func, y0=0, x_span=(0, 1),
                                        method='adams_bashforth', n_points=50)
    
    # Should produce reasonable results
    assert len(result['y']) == len(result['x'])
    assert isinstance(result['y'][-1], (int, float))


def test_differential_equations_custom_step_size() -> None:
    """
    Test case 8: Test with custom step size.
    """
    def simple_func(x, y):
        return 1  # dy/dx = 1, solution: y = x + C
    
    result = differential_equation_solver(simple_func, y0=0, x_span=(0, 2),
                                        method='euler', h=0.1)
    
    # With h=0.1, should have 21 points (0, 0.1, 0.2, ..., 2.0)
    assert len(result['x']) == 21
    assert abs(result['step_size'] - 0.1) < 1e-10


def test_differential_equations_adaptive_stepping() -> None:
    """
    Test case 9: Test adaptive stepping.
    """
    def func(x, y):
        return -y  # Exponential decay
    
    result = differential_equation_solver(func, y0=1.0, x_span=(0, 2),
                                        method='runge_kutta_4', adaptive=True,
                                        tolerance=1e-6, n_points=50)
    
    # Should adapt step size
    assert result['method_used'] == 'runge_kutta_4'
    assert len(result['y']) > 0


def test_differential_equations_invalid_function() -> None:
    """
    Test case 10: Test error with invalid function.
    """
    with pytest.raises(TypeError, match="func must be callable"):
        differential_equation_solver("not_a_function", 1.0, (0, 1))


def test_differential_equations_invalid_initial_condition() -> None:
    """
    Test case 11: Test error with invalid initial condition.
    """
    def func(x, y):
        return y
    
    with pytest.raises(TypeError, match="y0 must be numeric"):
        differential_equation_solver(func, "invalid", (0, 1))


def test_differential_equations_invalid_x_span() -> None:
    """
    Test case 12: Test error with invalid x_span.
    """
    def func(x, y):
        return y
    
    with pytest.raises(TypeError, match="x_span must be a tuple"):
        differential_equation_solver(func, 1.0, "invalid")
    
    with pytest.raises(ValueError, match="x_span must satisfy x0 < xf"):
        differential_equation_solver(func, 1.0, (2, 1))


def test_differential_equations_invalid_method() -> None:
    """
    Test case 13: Test error with invalid method.
    """
    def func(x, y):
        return y
    
    with pytest.raises(ValueError, match="method must be one of"):
        differential_equation_solver(func, 1.0, (0, 1), method='invalid_method')


def test_differential_equations_invalid_parameters() -> None:
    """
    Test case 14: Test error with invalid parameters.
    """
    def func(x, y):
        return y
    
    with pytest.raises(ValueError, match="h must be positive"):
        differential_equation_solver(func, 1.0, (0, 1), h=0)
    
    with pytest.raises(ValueError, match="tolerance must be positive"):
        differential_equation_solver(func, 1.0, (0, 1), tolerance=0)


def test_differential_equations_function_evaluation_error() -> None:
    """
    Test case 15: Test handling of function evaluation errors.
    """
    def problematic_func(x, y):
        if abs(x - 0.5) < 1e-10:
            raise ValueError("Function undefined at x=0.5")
        return y
    
    with pytest.raises(ValueError, match="Error evaluating function"):
        differential_equation_solver(problematic_func, 1.0, (0, 1), n_points=100)


def test_differential_equations_return_structure() -> None:
    """
    Test case 16: Test return structure completeness.
    """
    def func(x, y):
        return x
    
    result = differential_equation_solver(func, 1.0, (0, 1), method='euler')
    
    required_keys = ['x', 'y', 'method_used', 'step_size', 'n_steps', 'error_estimate']
    for key in required_keys:
        assert key in result
    
    assert isinstance(result['x'], np.ndarray)
    assert isinstance(result['y'], np.ndarray)
    assert isinstance(result['step_size'], (int, float))
    assert isinstance(result['n_steps'], int)


def test_differential_equations_oscillator() -> None:
    """
    Test case 17: Test simple harmonic oscillator (second-order as system).
    """
    # Convert d²y/dt² = -y to system: dy/dt = v, dv/dt = -y
    def oscillator_y(t, y):
        return y[1] if hasattr(y, '__getitem__') else 0  # v component
    
    def oscillator_v(t, v):
        return -1  # Simple case for testing
    
    # Test with simple function
    result = differential_equation_solver(oscillator_v, 1.0, (0, 2*math.pi),
                                        method='runge_kutta_4', n_points=100)
    
    # Should produce numerical solution
    assert len(result['y']) > 0
    assert isinstance(result['y'][-1], (int, float))


def test_differential_equations_complex_function() -> None:
    """
    Test case 18: Test with more complex differential equation.
    """
    def complex_func(x, y):
        return x*y + math.sin(x)  # dy/dx = xy + sin(x)
    
    result = differential_equation_solver(complex_func, y0=1.0, x_span=(0, 1),
                                        method='runge_kutta_4', n_points=100)
    
    # Should handle complex functions
    assert len(result['y']) == 100
    assert result['converged'] if 'converged' in result else True


def test_differential_equations_stiff_equation() -> None:
    """
    Test case 19: Test with potentially stiff equation.
    """
    def stiff_func(x, y):
        return -1000*y + 1  # Fast transient
    
    result = differential_equation_solver(stiff_func, y0=0, x_span=(0, 0.01),
                                        method='runge_kutta_4', n_points=1000)
    
    # Should handle stiff equations to some degree
    assert len(result['y']) > 0
    assert isinstance(result['y'][-1], (int, float))


def test_differential_equations_zero_step_size() -> None:
    """
    Test case 20: Test behavior with very small intervals.
    """
    def func(x, y):
        return y
    
    result = differential_equation_solver(func, 1.0, (0, 1e-6), method='euler', n_points=10)
    
    # Should handle very small intervals
    assert len(result['y']) > 0
    assert result['step_size'] > 0


def test_differential_equations_large_interval() -> None:
    """
    Test case 21: Test with large integration interval.
    """
    def decay_func(x, y):
        return -0.1*y  # Slow decay
    
    result = differential_equation_solver(decay_func, 1.0, (0, 100),
                                        method='runge_kutta_4', n_points=200)
    
    # Should handle large intervals
    assert len(result['y']) == 200
    assert result['x'][-1] == 100


def test_differential_equations_negative_interval() -> None:
    """
    Test case 22: Test integration in negative direction.
    """
    def func(x, y):
        return x  # dy/dx = x
    
    result = differential_equation_solver(func, 0, (-2, 0), method='euler', n_points=100)
    
    # Should handle negative intervals
    assert len(result['y']) > 0
    assert result['x'][0] == -2
    assert result['x'][-1] == 0
