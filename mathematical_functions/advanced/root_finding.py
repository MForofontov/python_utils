"""
Root finding algorithms for finding zeros of functions.

This module provides various numerical methods for finding roots (zeros)
of mathematical functions using different algorithms.
"""

import math
from typing import Union, Callable, Dict, Any, Optional, Tuple


def root_finding(func: Callable[[float], float],
                a: float,
                b: Optional[float] = None,
                method: str = 'bisection',
                tolerance: float = 1e-8,
                max_iterations: int = 1000,
                **kwargs) -> Dict[str, Any]:
    """
    Find roots of a function using various numerical methods.

    Finds zeros of a continuous function using different root-finding algorithms.
    Some methods require an interval [a, b], others only need an initial guess.

    Parameters
    ----------
    func : callable
        Function for which to find roots. Must take a single float argument.
    a : float
        Left endpoint of interval (for bracketing methods) or initial guess (for open methods).
    b : float, optional
        Right endpoint of interval (required for bracketing methods).
    method : str, optional
        Root-finding method to use. Options:
        - 'bisection': Bisection method (requires interval) (default)
        - 'newton': Newton-Raphson method (requires initial guess)
        - 'secant': Secant method (requires initial guess)
        - 'false_position': False position (regula falsi) method (requires interval)
        - 'brentq': Brent's method (requires interval)
        - 'illinois': Illinois method (requires interval)
    tolerance : float, optional
        Convergence tolerance for root (default: 1e-8).
    max_iterations : int, optional
        Maximum number of iterations (default: 1000).
    **kwargs : dict
        Additional parameters for specific methods:
        - derivative : callable, derivative function for Newton's method
        - x1 : float, second initial guess for secant method

    Returns
    -------
    dict
        Dictionary containing:
        - 'root': Found root value
        - 'function_value': Function value at root
        - 'iterations': Number of iterations used
        - 'converged': Whether method converged
        - 'method_used': Root-finding method used
        - 'bracket': Final bracket interval (for bracketing methods)

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid or method requirements not met.

    Examples
    --------
    >>> import math
    >>> # Find root of x^2 - 2 (should be sqrt(2))
    >>> result = root_finding(lambda x: x**2 - 2, 0, 3)
    >>> abs(result['root'] - math.sqrt(2)) < 1e-6
    True
    >>> result['converged']
    True

    Notes
    -----
    Bracketing methods (bisection, false_position, brentq) are more robust
    but require an interval where the function changes sign. Open methods
    (newton, secant) converge faster but may not converge without good initial guess.
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(a, (int, float)):
        raise TypeError("a must be numeric")
    if b is not None and not isinstance(b, (int, float)):
        raise TypeError("b must be numeric or None")
    if not isinstance(tolerance, (int, float)) or tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be positive integer")
    
    # Validate method
    bracketing_methods = ['bisection', 'false_position', 'brentq', 'illinois']
    open_methods = ['newton', 'secant']
    valid_methods = bracketing_methods + open_methods
    
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    method = method.lower()
    
    # Check method requirements
    if method in bracketing_methods and b is None:
        raise ValueError(f"{method} method requires both a and b parameters")
    
    if method in bracketing_methods:
        if a >= b:
            raise ValueError("for bracketing methods, a must be less than b")
        
        # Test function at endpoints
        try:
            fa = func(a)
            fb = func(b)
        except Exception as e:
            raise ValueError(f"function evaluation failed: {str(e)}")
        
        if not isinstance(fa, (int, float)) or not isinstance(fb, (int, float)):
            raise ValueError("function must return numeric values")
        
        # Check for sign change
        if fa * fb > 0:
            raise ValueError(f"function must have different signs at a={a} (f(a)={fa}) and b={b} (f(b)={fb})")
    
    # Apply root-finding method
    if method == 'bisection':
        return _bisection_method(func, a, b, tolerance, max_iterations)
    elif method == 'newton':
        derivative = kwargs.get('derivative', None)
        return _newton_method(func, a, tolerance, max_iterations, derivative)
    elif method == 'secant':
        x1 = kwargs.get('x1', a + 0.1)  # Default second point
        return _secant_method(func, a, x1, tolerance, max_iterations)
    elif method == 'false_position':
        return _false_position_method(func, a, b, tolerance, max_iterations)
    elif method == 'brentq':
        return _brent_method(func, a, b, tolerance, max_iterations)
    elif method == 'illinois':
        return _illinois_method(func, a, b, tolerance, max_iterations)


def _bisection_method(func: Callable, a: float, b: float, 
                     tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Bisection method implementation."""
    fa = func(a)
    fb = func(b)
    
    for iteration in range(max_iterations):
        c = (a + b) / 2.0
        fc = func(c)
        
        if abs(fc) < tolerance or (b - a) / 2 < tolerance:
            return {
                'root': c,
                'function_value': fc,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'bisection',
                'bracket': (a, b)
            }
        
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    c = (a + b) / 2.0
    return {
        'root': c,
        'function_value': func(c),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'bisection',
        'bracket': (a, b)
    }


def _newton_method(func: Callable, x0: float, tolerance: float, 
                  max_iterations: int, derivative: Optional[Callable] = None) -> Dict[str, Any]:
    """Newton-Raphson method implementation."""
    
    def numerical_derivative(f, x, h=1e-8):
        """Calculate numerical derivative."""
        return (f(x + h) - f(x - h)) / (2 * h)
    
    x = x0
    
    for iteration in range(max_iterations):
        fx = func(x)
        
        if abs(fx) < tolerance:
            return {
                'root': x,
                'function_value': fx,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'newton',
                'bracket': None
            }
        
        # Calculate derivative
        if derivative:
            fpx = derivative(x)
        else:
            fpx = numerical_derivative(func, x)
        
        if abs(fpx) < 1e-12:
            # Derivative too small, method may not converge
            break
        
        x_new = x - fx / fpx
        
        if abs(x_new - x) < tolerance:
            return {
                'root': x_new,
                'function_value': func(x_new),
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'newton',
                'bracket': None
            }
        
        x = x_new
    
    return {
        'root': x,
        'function_value': func(x),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'newton',
        'bracket': None
    }


def _secant_method(func: Callable, x0: float, x1: float, 
                  tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Secant method implementation."""
    
    for iteration in range(max_iterations):
        f0 = func(x0)
        f1 = func(x1)
        
        if abs(f1) < tolerance:
            return {
                'root': x1,
                'function_value': f1,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'secant',
                'bracket': None
            }
        
        if abs(f1 - f0) < 1e-12:
            # Denominator too small
            break
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        
        if abs(x2 - x1) < tolerance:
            return {
                'root': x2,
                'function_value': func(x2),
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'secant',
                'bracket': None
            }
        
        x0, x1 = x1, x2
    
    return {
        'root': x1,
        'function_value': func(x1),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'secant',
        'bracket': None
    }


def _false_position_method(func: Callable, a: float, b: float,
                          tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """False position (regula falsi) method implementation."""
    fa = func(a)
    fb = func(b)
    
    for iteration in range(max_iterations):
        # Calculate false position point
        c = (a * fb - b * fa) / (fb - fa)
        fc = func(c)
        
        if abs(fc) < tolerance or abs(b - a) < tolerance:
            return {
                'root': c,
                'function_value': fc,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'false_position',
                'bracket': (a, b)
            }
        
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    c = (a * fb - b * fa) / (fb - fa)
    return {
        'root': c,
        'function_value': func(c),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'false_position',
        'bracket': (a, b)
    }


def _brent_method(func: Callable, a: float, b: float,
                 tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Brent's method implementation (simplified version)."""
    # This is a simplified version of Brent's method
    # Full implementation would include inverse quadratic interpolation
    
    fa = func(a)
    fb = func(b)
    
    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa
    
    c = a
    fc = fa
    mflag = True
    
    for iteration in range(max_iterations):
        if abs(fb) < tolerance:
            return {
                'root': b,
                'function_value': fb,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'brentq',
                'bracket': (a, b)
            }
        
        if fa != fc and fb != fc:
            # Inverse quadratic interpolation
            s = (a * fb * fc) / ((fa - fb) * (fa - fc)) + \
                (b * fa * fc) / ((fb - fa) * (fb - fc)) + \
                (c * fa * fb) / ((fc - fa) * (fc - fb))
        else:
            # Secant method
            s = b - fb * (b - a) / (fb - fa)
        
        # Check conditions for accepting s
        tmp2 = (3 * a + b) / 4
        if not ((s > tmp2 and s < b) or (s < tmp2 and s > b)):
            mflag = True
        elif mflag and abs(s - b) >= abs(b - c) / 2:
            mflag = True
        elif not mflag and abs(s - b) >= abs(c - a) / 2:
            mflag = True
        elif mflag and abs(b - c) < tolerance:
            mflag = True
        elif not mflag and abs(c - a) < tolerance:
            mflag = True
        else:
            mflag = False
        
        if mflag:
            s = (a + b) / 2
            mflag = True
        else:
            mflag = False
        
        fs = func(s)
        a, fa = b, fb
        
        if fa * fs < 0:
            b, fb = s, fs
        else:
            a, fa = s, fs
        
        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa
        
        c = a
        fc = fa
    
    return {
        'root': b,
        'function_value': fb,
        'iterations': max_iterations,
        'converged': abs(fb) < tolerance,
        'method_used': 'brentq',
        'bracket': (a, b)
    }


def _illinois_method(func: Callable, a: float, b: float,
                    tolerance: float, max_iterations: int) -> Dict[str, Any]:
    """Illinois method implementation."""
    fa = func(a)
    fb = func(b)
    side = 0
    
    for iteration in range(max_iterations):
        c = (fa * b - fb * a) / (fa - fb)
        fc = func(c)
        
        if abs(fc) < tolerance or abs(b - a) < tolerance:
            return {
                'root': c,
                'function_value': fc,
                'iterations': iteration + 1,
                'converged': True,
                'method_used': 'illinois',
                'bracket': (a, b)
            }
        
        if fa * fc > 0:
            a = c
            fa = fc
            if side == -1:
                fb /= 2
            side = -1
        else:
            b = c
            fb = fc
            if side == 1:
                fa /= 2
            side = 1
    
    c = (fa * b - fb * a) / (fa - fb)
    return {
        'root': c,
        'function_value': func(c),
        'iterations': max_iterations,
        'converged': False,
        'method_used': 'illinois',
        'bracket': (a, b)
    }


__all__ = ['root_finding']
