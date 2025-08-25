"""
Optimization algorithms for finding function minima and maxima.

This module provides various optimization methods for finding optimal values
of mathematical functions using different algorithms.
"""

import math
from typing import Union, Callable, Dict, Any, Optional, Tuple, List


def optimization(func: Callable[[float], float],
                bounds: Tuple[float, float],
                method: str = 'golden_section',
                maximize: bool = False,
                tolerance: float = 1e-8,
                max_iterations: int = 1000,
                **kwargs) -> Dict[str, Any]:
    """
    Find optimal value of a function using various optimization methods.

    Finds minimum or maximum of a univariate function within given bounds
    using different optimization algorithms.

    Parameters
    ----------
    func : callable
        Function to optimize. Must take a single float argument.
    bounds : tuple of float
        Tuple (a, b) defining search interval where a < b.
    method : str, optional
        Optimization method to use. Options:
        - 'golden_section': Golden section search (default)
        - 'ternary_search': Ternary search algorithm
        - 'brent': Brent's method for optimization
        - 'fibonacci': Fibonacci search method
        - 'parabolic': Parabolic interpolation method
        - 'grid_search': Grid search with refinement
    maximize : bool, optional
        If True, find maximum instead of minimum (default: False).
    tolerance : float, optional
        Convergence tolerance (default: 1e-8).
    max_iterations : int, optional
        Maximum number of iterations (default: 1000).
    **kwargs : dict
        Additional parameters for specific methods:
        - n_points : int, number of grid points for grid search (default: 100)
        - refinement_levels : int, refinement levels for grid search (default: 3)

    Returns
    -------
    dict
        Dictionary containing:
        - 'x_optimal': Optimal x value
        - 'f_optimal': Function value at optimal point
        - 'iterations': Number of iterations used
        - 'converged': Whether method converged
        - 'method_used': Optimization method used
        - 'function_evaluations': Total function evaluations
        - 'final_interval': Final search interval

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid.

    Examples
    --------
    >>> # Find minimum of x^2 - 4x + 3 (should be at x=2, f=−1)
    >>> result = optimization(lambda x: x**2 - 4*x + 3, (-10, 10))
    >>> abs(result['x_optimal'] - 2.0) < 1e-6
    True
    >>> abs(result['f_optimal'] - (-1.0)) < 1e-6
    True

    Notes
    -----
    Golden section search and ternary search work for unimodal functions.
    Brent's method combines golden section with parabolic interpolation.
    Grid search is more robust but computationally expensive.
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(bounds, (tuple, list)) or len(bounds) != 2:
        raise TypeError("bounds must be a tuple or list of length 2")
    
    a, b = bounds
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("bounds must contain numeric values")
    if a >= b:
        raise ValueError("bounds must satisfy a < b")
    
    if not isinstance(tolerance, (int, float)) or tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be positive integer")
    
    # Validate method
    valid_methods = ['golden_section', 'ternary_search', 'brent', 'fibonacci', 'parabolic', 'grid_search']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    method = method.lower()
    
    # Handle maximization by negating function
    if maximize:
        original_func = func
        func = lambda x: -original_func(x)
    
    # Apply optimization method
    if method == 'golden_section':
        result = _golden_section_search(func, a, b, tolerance, max_iterations)
    elif method == 'ternary_search':
        result = _ternary_search(func, a, b, tolerance, max_iterations)
    elif method == 'brent':
        result = _brent_optimization(func, a, b, tolerance, max_iterations)
    elif method == 'fibonacci':
        result = _fibonacci_search(func, a, b, tolerance, max_iterations)
    elif method == 'parabolic':
        result = _parabolic_interpolation(func, a, b, tolerance, max_iterations)
    elif method == 'grid_search':
        n_points = kwargs.get('n_points', 100)
        refinement_levels = kwargs.get('refinement_levels', 3)
        result = _grid_search_optimization(func, a, b, tolerance, max_iterations, n_points, refinement_levels)
    
    # Handle maximization results
    if maximize:
        result['f_optimal'] = -result['f_optimal']
    
    return result


def _golden_section_search(func: Callable, a: float, b: float,
                          tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Golden section search implementation."""
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio
    resphi = 2 - phi  # 1/phi
    
    # Initial points
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1 = func(x1)
    f2 = func(x2)
    function_evals = 2
    
    for iteration in range(max_iterations):
        if abs(b - a) < tolerance:
            x_optimal = (a + b) / 2
            return {
                'x_optimal': x_optimal,
                'f_optimal': func(x_optimal),
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'golden_section',
                'function_evaluations': function_evals + 1,
                'final_interval': (a, b)
            }
        
        if f2 > f1:  # f1 < f2, minimum is in [a, x2]
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = func(x1)
        else:  # f1 >= f2, minimum is in [x1, b]
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = func(x2)
        
        function_evals += 1
    
    x_optimal = (a + b) / 2
    return {
        'x_optimal': x_optimal,
        'f_optimal': func(x_optimal),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'golden_section',
        'function_evaluations': function_evals + 1,
        'final_interval': (a, b)
    }


def _ternary_search(func: Callable, a: float, b: float,
                   tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Ternary search implementation."""
    function_evals = 0
    
    for iteration in range(max_iterations):
        if abs(b - a) < tolerance:
            x_optimal = (a + b) / 2
            return {
                'x_optimal': x_optimal,
                'f_optimal': func(x_optimal),
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'ternary_search',
                'function_evaluations': function_evals + 1,
                'final_interval': (a, b)
            }
        
        # Divide interval into three parts
        m1 = a + (b - a) / 3
        m2 = b - (b - a) / 3
        
        f1 = func(m1)
        f2 = func(m2)
        function_evals += 2
        
        if f1 > f2:  # Minimum is in [m1, b]
            a = m1
        else:  # Minimum is in [a, m2]
            b = m2
    
    x_optimal = (a + b) / 2
    return {
        'x_optimal': x_optimal,
        'f_optimal': func(x_optimal),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'ternary_search',
        'function_evaluations': function_evals + 1,
        'final_interval': (a, b)
    }


def _brent_optimization(func: Callable, a: float, b: float,
                       tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Brent's method for optimization (simplified version)."""
    phi = (3 - math.sqrt(5)) / 2  # Golden ratio conjugate
    
    # Initial setup
    x = w = v = (a + b) / 2  # Best, second best, third best points
    fx = fw = fv = func(x)
    function_evals = 1
    
    d = e = 0.0  # Step sizes
    
    for iteration in range(max_iterations):
        m = (a + b) / 2  # Midpoint
        tol1 = tolerance * abs(x) + 1e-10
        tol2 = 2 * tol1
        
        if abs(x - m) <= (tol2 - (b - a) / 2):
            return {
                'x_optimal': x,
                'f_optimal': fx,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'brent',
                'function_evaluations': function_evals,
                'final_interval': (a, b)
            }
        
        # Try parabolic interpolation
        if abs(e) > tol1:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2 * (q - r)
            
            if q > 0:
                p = -p
            q = abs(q)
            
            # Check if parabolic step is acceptable
            if abs(p) < abs(0.5 * q * e) and p > q * (a - x) and p < q * (b - x):
                e = d
                d = p / q  # Parabolic step
                u = x + d
                
                if (u - a) < tol2 or (b - u) < tol2:
                    d = tol1 if x < m else -tol1
            else:
                # Golden section step
                e = (b - x) if x < m else (a - x)
                d = phi * e
        else:
            # Golden section step
            e = (b - x) if x < m else (a - x)
            d = phi * e
        
        # Ensure step is not too small
        u = x + (d if abs(d) >= tol1 else (tol1 if d > 0 else -tol1))
        fu = func(u)
        function_evals += 1
        
        # Update points
        if fu <= fx:
            if u < x:
                b = x
            else:
                a = x
            v, w, x = w, x, u
            fv, fw, fx = fw, fx, fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v, fv = w, fw
                w, fw = u, fu
            elif fu <= fv or v == x or v == w:
                v, fv = u, fu
    
    return {
        'x_optimal': x,
        'f_optimal': fx,
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'brent',
        'function_evaluations': function_evals,
        'final_interval': (a, b)
    }


def _fibonacci_search(func: Callable, a: float, b: float,
                     tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Fibonacci search implementation."""
    # Generate Fibonacci numbers
    fib = [1, 1]
    while fib[-1] < (b - a) / tolerance:
        fib.append(fib[-1] + fib[-2])
    
    n = len(fib) - 1
    n = min(n, max_iterations)
    
    # Initial points
    L = b - a
    x1 = a + (fib[n-2] / fib[n]) * L
    x2 = a + (fib[n-1] / fib[n]) * L
    f1 = func(x1)
    f2 = func(x2)
    function_evals = 2
    
    for k in range(n - 2):
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            L = b - a
            x2 = a + (fib[n-k-2] / fib[n-k-1]) * L
            f2 = func(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            L = b - a
            x1 = a + (fib[n-k-3] / fib[n-k-1]) * L
            f1 = func(x1)
        
        function_evals += 1
    
    x_optimal = (a + b) / 2
    return {
        'x_optimal': x_optimal,
        'f_optimal': func(x_optimal),
        'iterations': n - 2,
        'converged': True,
        'method_used': 'fibonacci',
        'function_evaluations': function_evals + 1,
        'final_interval': (a, b)
    }


def _parabolic_interpolation(func: Callable, a: float, b: float,
                           tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Parabolic interpolation optimization."""
    # Initial three points
    x1 = a
    x3 = b
    x2 = (a + b) / 2
    
    f1 = func(x1)
    f2 = func(x2)
    f3 = func(x3)
    function_evals = 3
    
    for iteration in range(max_iterations):
        # Check convergence
        if abs(x3 - x1) < tolerance:
            # Find minimum among the three points
            if f1 <= f2 and f1 <= f3:
                x_min, f_min = x1, f1
            elif f2 <= f1 and f2 <= f3:
                x_min, f_min = x2, f2
            else:
                x_min, f_min = x3, f3
            
            return {
                'x_optimal': x_min,
                'f_optimal': f_min,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'parabolic',
                'function_evaluations': function_evals,
                'final_interval': (x1, x3)
            }
        
        # Parabolic interpolation
        denom = 2 * ((x1 - x2) * (f1 - f3) - (x1 - x3) * (f1 - f2))
        
        if abs(denom) < 1e-12:
            # Fall back to golden section step
            if x2 - x1 > x3 - x2:
                x_new = x1 + 0.618 * (x2 - x1)
            else:
                x_new = x2 + 0.618 * (x3 - x2)
        else:
            # Parabolic interpolation formula
            x_new = x1 - ((x1 - x2)**2 * (f1 - f3) - (x1 - x3)**2 * (f1 - f2)) / denom
            
            # Ensure new point is within bounds
            if x_new <= x1 or x_new >= x3:
                x_new = (x1 + x3) / 2
        
        f_new = func(x_new)
        function_evals += 1
        
        # Update points
        if x_new < x2:
            if f_new < f2:
                x3, f3 = x2, f2
                x2, f2 = x_new, f_new
            else:
                x1, f1 = x_new, f_new
        else:
            if f_new < f2:
                x1, f1 = x2, f2
                x2, f2 = x_new, f_new
            else:
                x3, f3 = x_new, f_new
    
    # Find minimum among final three points
    if f1 <= f2 and f1 <= f3:
        x_min, f_min = x1, f1
    elif f2 <= f1 and f2 <= f3:
        x_min, f_min = x2, f2
    else:
        x_min, f_min = x3, f3
    
    return {
        'x_optimal': x_min,
        'f_optimal': f_min,
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'parabolic',
        'function_evaluations': function_evals,
        'final_interval': (x1, x3)
    }


def _grid_search_optimization(func: Callable, a: float, b: float,
                            tolerance: float, max_iterations: int,
                            n_points: int, refinement_levels: int) -> Dict[str, Any]:
    """Grid search with iterative refinement."""
    function_evals = 0
    current_a, current_b = a, b
    
    for level in range(refinement_levels):
        # Create grid points
        x_values = [current_a + i * (current_b - current_a) / (n_points - 1) for i in range(n_points)]
        f_values = [func(x) for x in x_values]
        function_evals += n_points
        
        # Find minimum
        min_idx = f_values.index(min(f_values))
        x_min = x_values[min_idx]
        f_min = f_values[min_idx]
        
        # Check convergence
        if current_b - current_a < tolerance:
            return {
                'x_optimal': x_min,
                'f_optimal': f_min,
                'iterations': level + 1,
                'converged': True,
                'method_used': 'grid_search',
                'function_evaluations': function_evals,
                'final_interval': (current_a, current_b)
            }
        
        # Refine interval around minimum
        if min_idx == 0:
            current_b = x_values[1]
        elif min_idx == n_points - 1:
            current_a = x_values[-2]
        else:
            current_a = x_values[min_idx - 1]
            current_b = x_values[min_idx + 1]
    
    return {
        'x_optimal': x_min,
        'f_optimal': f_min,
        'iterations': refinement_levels,
        'converged': current_b - current_a < tolerance,
        'method_used': 'grid_search',
        'function_evaluations': function_evals,
        'final_interval': (current_a, current_b)
    }


__all__ = ['optimization']
