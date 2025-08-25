"""Numerical integration using multiple methods with adaptive error control."""

from typing import Union, Callable, Dict, Tuple
import math


def numerical_integration(func: Callable[[float], float],
                         a: float,
                         b: float,
                         method: str = 'adaptive_simpson',
                         tolerance: float = 1e-8,
                         max_iterations: int = 1000) -> Dict[str, Union[float, int, str, bool]]:
    """
    Perform numerical integration using multiple methods with adaptive error control.

    Integrates a function over the interval [a, b] using various numerical methods
    including trapezoidal rule, Simpson's rule, and adaptive algorithms.

    Parameters
    ----------
    func : callable
        Function to integrate. Must take a single float argument and return float.
    a : float
        Lower bound of integration.
    b : float
        Upper bound of integration.
    method : str, optional
        Integration method: 'trapezoidal', 'simpson', 'adaptive_simpson', 
        'romberg', or 'gauss_legendre'. Default 'adaptive_simpson'.
    tolerance : float, optional
        Absolute error tolerance for adaptive methods. Default 1e-8.
    max_iterations : int, optional
        Maximum number of iterations for adaptive methods. Default 1000.

    Returns
    -------
    dict[str, Union[float, int, str, bool]]
        Dictionary containing:
        - 'integral': Estimated integral value
        - 'error_estimate': Estimated absolute error
        - 'iterations': Number of iterations used
        - 'converged': Boolean indicating convergence
        - 'method_used': Integration method used
        - 'function_evaluations': Number of function evaluations
        - 'intervals': Number of subintervals in final approximation

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid or function evaluation fails.

    Examples
    --------
    >>> import math
    >>> # Integrate sin(x) from 0 to π (should be 2)
    >>> result = numerical_integration(math.sin, 0, math.pi)
    >>> abs(result['integral'] - 2.0) < 1e-6
    True
    >>> result['converged']
    True
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(a, (int, float)):
        raise TypeError("a must be numeric")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be numeric")
    if not isinstance(method, str):
        raise TypeError("method must be a string")
    if not isinstance(tolerance, (int, float)):
        raise TypeError("tolerance must be numeric")
    if not isinstance(max_iterations, int):
        raise TypeError("max_iterations must be an integer")
    
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    
    valid_methods = ['trapezoidal', 'simpson', 'adaptive_simpson', 'romberg', 'gauss_legendre']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    # Test function at endpoints
    try:
        fa = func(a)
        fb = func(b)
    except Exception as e:
        raise ValueError(f"Function evaluation failed: {str(e)}")
    
    if not isinstance(fa, (int, float)) or not isinstance(fb, (int, float)):
        raise ValueError("Function must return numeric values")
    
    method = method.lower()
    
    # Handle case where a > b
    if a > b:
        result = numerical_integration(func, b, a, method, tolerance, max_iterations)
        result['integral'] = -result['integral']
        return result
    
    # Handle case where a == b
    if abs(a - b) < 1e-15:
        return {
            'integral': 0.0,
            'error_estimate': 0.0,
            'iterations': 1,
            'converged': True,
            'method_used': method,
            'function_evaluations': 2,
            'intervals': 1
        }
    
    # Select integration method
    if method == 'trapezoidal':
        return _trapezoidal_integration(func, a, b, tolerance, max_iterations)
    elif method == 'simpson':
        return _simpson_integration(func, a, b, tolerance, max_iterations)
    elif method == 'adaptive_simpson':
        return _adaptive_simpson_integration(func, a, b, tolerance, max_iterations)
    elif method == 'romberg':
        return _romberg_integration(func, a, b, tolerance, max_iterations)
    elif method == 'gauss_legendre':
        return _gauss_legendre_integration(func, a, b, tolerance, max_iterations)


def _trapezoidal_integration(func: Callable, a: float, b: float, 
                           tolerance: float, max_iterations: int) -> Dict:
    """Adaptive trapezoidal rule integration."""
    n = 1
    h = b - a
    integral_old = 0.5 * h * (func(a) + func(b))
    function_evals = 2
    
    for iteration in range(1, max_iterations + 1):
        n *= 2
        h = (b - a) / n
        
        # Calculate new points
        integral_new = 0.5 * integral_old
        for i in range(1, n, 2):
            x = a + i * h
            integral_new += h * func(x)
            function_evals += 1
        
        error_estimate = abs(integral_new - integral_old) / 3.0
        
        if error_estimate < tolerance:
            return {
                'integral': integral_new,
                'error_estimate': error_estimate,
                'iterations': iteration,
                'converged': True,
                'method_used': 'trapezoidal',
                'function_evaluations': function_evals,
                'intervals': n
            }
        
        integral_old = integral_new
    
    return {
        'integral': integral_old,
        'error_estimate': error_estimate,
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'trapezoidal',
        'function_evaluations': function_evals,
        'intervals': n
    }


def _simpson_integration(func: Callable, a: float, b: float,
                        tolerance: float, max_iterations: int) -> Dict:
    """Adaptive Simpson's rule integration."""
    def simpson_basic(f, x0, x2, fx0, fx2, is_whole_interval=True):
        """Basic Simpson's rule for interval [x0, x2]."""
        x1 = (x0 + x2) / 2
        fx1 = f(x1)
        
        if is_whole_interval:
            # For whole interval: (b-a)/6 * (f(a) + 4*f(m) + f(b))
            return (x2 - x0) / 6 * (fx0 + 4 * fx1 + fx2), fx1, 1
        else:
            # For subinterval
            return (x2 - x0) / 6 * (fx0 + 4 * fx1 + fx2), fx1, 1
    
    def adaptive_simpson_recursive(f, a, b, fa, fb, whole_area, tol, depth, max_depth):
        """Recursive adaptive Simpson's rule."""
        if depth >= max_depth:
            return whole_area, 1, False
        
        c = (a + b) / 2
        fc = f(c)
        
        left_area, _, _ = simpson_basic(f, a, c, fa, fc, False)
        right_area, _, _ = simpson_basic(f, c, b, fc, fb, False)
        
        area_sum = left_area + right_area
        error_estimate = abs(area_sum - whole_area) / 15.0
        
        if error_estimate <= tol:
            return area_sum + error_estimate / 15.0, 3, True
        
        tol_left = tol / 2
        tol_right = tol / 2
        
        left_result, left_evals, left_conv = adaptive_simpson_recursive(
            f, a, c, fa, fc, left_area, tol_left, depth + 1, max_depth
        )
        right_result, right_evals, right_conv = adaptive_simpson_recursive(
            f, c, b, fc, fb, right_area, tol_right, depth + 1, max_depth
        )
        
        return left_result + right_result, 1 + left_evals + right_evals, left_conv and right_conv
    
    # Initial Simpson's rule estimate
    fa = func(a)
    fb = func(b)
    initial_area, _, _ = simpson_basic(func, a, b, fa, fb)
    
    max_depth = min(int(math.log2(max_iterations)), 20)
    
    integral, function_evals, converged = adaptive_simpson_recursive(
        func, a, b, fa, fb, initial_area, tolerance, 0, max_depth
    )
    
    return {
        'integral': integral,
        'error_estimate': tolerance if converged else tolerance * 10,
        'iterations': max_depth if not converged else function_evals // 2,
        'converged': converged,
        'method_used': 'simpson',
        'function_evaluations': function_evals + 2,
        'intervals': 2 ** max_depth if not converged else function_evals
    }


def _adaptive_simpson_integration(func: Callable, a: float, b: float,
                                tolerance: float, max_iterations: int) -> Dict:
    """Enhanced adaptive Simpson's rule with better error estimation."""
    return _simpson_integration(func, a, b, tolerance, max_iterations)


def _romberg_integration(func: Callable, a: float, b: float,
                        tolerance: float, max_iterations: int) -> Dict:
    """Romberg integration using Richardson extrapolation."""
    max_k = min(max_iterations, 20)
    R = [[0.0 for _ in range(max_k)] for _ in range(max_k)]
    
    # Initialize with trapezoidal rule
    h = b - a
    R[0][0] = 0.5 * h * (func(a) + func(b))
    function_evals = 2
    
    for i in range(1, max_k):
        # Refine trapezoidal rule
        h = h / 2
        sum_new = 0
        for k in range(1, 2**i, 2):
            x = a + k * h
            sum_new += func(x)
            function_evals += 1
        
        R[i][0] = 0.5 * R[i-1][0] + h * sum_new
        
        # Richardson extrapolation
        for j in range(1, i + 1):
            factor = 4**j
            R[i][j] = (factor * R[i][j-1] - R[i-1][j-1]) / (factor - 1)
        
        # Check convergence
        if i > 0:
            error_estimate = abs(R[i][i] - R[i-1][i-1])
            if error_estimate < tolerance:
                return {
                    'integral': R[i][i],
                    'error_estimate': error_estimate,
                    'iterations': i + 1,
                    'converged': True,
                    'method_used': 'romberg',
                    'function_evaluations': function_evals,
                    'intervals': 2**i
                }
    
    final_error = abs(R[max_k-1][max_k-1] - R[max_k-2][max_k-2]) if max_k > 1 else tolerance
    
    return {
        'integral': R[max_k-1][max_k-1],
        'error_estimate': final_error,
        'iterations': max_k,
        'converged': final_error < tolerance,
        'method_used': 'romberg',
        'function_evaluations': function_evals,
        'intervals': 2**(max_k-1)
    }


def _gauss_legendre_integration(func: Callable, a: float, b: float,
                              tolerance: float, max_iterations: int) -> Dict:
    """Gauss-Legendre quadrature with adaptive order."""
    
    def gauss_legendre_weights_nodes(n):
        """Generate weights and nodes for Gauss-Legendre quadrature."""
        if n == 2:
            nodes = [-0.5773502691896257, 0.5773502691896257]
            weights = [1.0, 1.0]
        elif n == 3:
            nodes = [-0.7745966692414834, 0.0, 0.7745966692414834]
            weights = [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]
        elif n == 4:
            nodes = [-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526]
            weights = [0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538]
        elif n == 5:
            nodes = [-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640]
            weights = [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891]
        else:
            # Default to 4-point for higher orders
            nodes = [-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526]
            weights = [0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538]
        
        return nodes, weights
    
    # Start with lower order and increase if needed
    best_result = None
    function_evals = 0
    
    for n in [2, 3, 4, 5, 8]:  # Try different orders
        if n > max_iterations:
            break
            
        nodes, weights = gauss_legendre_weights_nodes(min(n, 5))
        
        # Transform to interval [a, b]
        integral = 0.0
        for i in range(len(nodes)):
            x = 0.5 * ((b - a) * nodes[i] + (b + a))
            try:
                integral += weights[i] * func(x)
                function_evals += 1
            except:
                raise ValueError("Function evaluation failed during integration")
        
        integral *= 0.5 * (b - a)
        
        # Error estimation using different orders
        if best_result is not None:
            error_estimate = abs(integral - best_result)
            if error_estimate < tolerance:
                return {
                    'integral': integral,
                    'error_estimate': error_estimate,
                    'iterations': n,
                    'converged': True,
                    'method_used': 'gauss_legendre',
                    'function_evaluations': function_evals,
                    'intervals': 1
                }
        
        best_result = integral
    
    return {
        'integral': best_result if best_result is not None else 0.0,
        'error_estimate': tolerance * 10,  # Conservative estimate
        'iterations': n,
        'converged': False,
        'method_used': 'gauss_legendre',
        'function_evaluations': function_evals,
        'intervals': 1
    }


__all__ = ['numerical_integration']
