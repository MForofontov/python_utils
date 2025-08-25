"""
Numerical methods for solving ordinary differential equations.

This module provides various algorithms for solving initial value problems
and boundary value problems for ordinary differential equations.
"""

import math
from typing import Union, Callable, Dict, Any, Optional, Tuple, List
import numpy as np


def differential_equation_solver(func: Callable[[float, float], float],
                                y0: float,
                                x_span: Tuple[float, float],
                                method: str = 'runge_kutta_4',
                                h: Optional[float] = None,
                                n_points: Optional[int] = None,
                                tolerance: float = 1e-8,
                                adaptive: bool = False) -> Dict[str, Any]:
    """
    Solve ordinary differential equations using various numerical methods.

    Solves initial value problems of the form dy/dx = f(x, y) with y(x0) = y0
    using different numerical integration methods.

    Parameters
    ----------
    func : callable
        Function f(x, y) representing dy/dx = f(x, y).
    y0 : float
        Initial condition y(x0) = y0.
    x_span : tuple of float
        Integration interval (x0, xf) where x0 < xf.
    method : str, optional
        Numerical method to use. Options:
        - 'euler': Forward Euler method (default)
        - 'modified_euler': Modified Euler (Heun's) method
        - 'runge_kutta_4': Fourth-order Runge-Kutta method
        - 'runge_kutta_2': Second-order Runge-Kutta method
        - 'midpoint': Midpoint method
        - 'adams_bashforth': Adams-Bashforth multi-step method
    h : float, optional
        Step size. If None, computed from n_points.
    n_points : int, optional
        Number of points (default: 100). Ignored if h is provided.
    tolerance : float, optional
        Error tolerance for adaptive methods (default: 1e-8).
    adaptive : bool, optional
        Use adaptive step size (default: False).

    Returns
    -------
    dict
        Dictionary containing:
        - 'x': Array of x values
        - 'y': Array of y values  
        - 'method_used': Integration method used
        - 'step_size': Step size used (average if adaptive)
        - 'n_steps': Number of integration steps
        - 'error_estimate': Final error estimate (if available)

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid.

    Examples
    --------
    >>> # Solve dy/dx = -y, y(0) = 1 (exact solution: y = exp(-x))
    >>> result = differential_equation_solver(lambda x, y: -y, 1.0, (0, 2))
    >>> x_final = result['x'][-1]
    >>> y_final = result['y'][-1]
    >>> exact = math.exp(-x_final)
    >>> abs(y_final - exact) < 0.01
    True

    Notes
    -----
    Runge-Kutta methods generally provide better accuracy than Euler methods.
    Adams-Bashforth methods are efficient for smooth solutions but require
    startup using Runge-Kutta method for initial points.
    """
    # Input validation
    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(y0, (int, float)):
        raise TypeError("y0 must be numeric")
    if not isinstance(x_span, (tuple, list)) or len(x_span) != 2:
        raise TypeError("x_span must be a tuple or list of length 2")
    
    x0, xf = x_span
    if not isinstance(x0, (int, float)) or not isinstance(xf, (int, float)):
        raise TypeError("x_span must contain numeric values")
    if x0 >= xf:
        raise ValueError("x_span must satisfy x0 < xf")
    
    # Validate method
    valid_methods = ['euler', 'modified_euler', 'runge_kutta_4', 'runge_kutta_2', 
                     'midpoint', 'adams_bashforth']
    if method.lower() not in valid_methods:
        raise ValueError(f"method must be one of {valid_methods}")
    
    method = method.lower()
    
    # Determine step size
    if h is None:
        if n_points is None:
            n_points = 100
        h = (xf - x0) / (n_points - 1)
    else:
        if not isinstance(h, (int, float)) or h <= 0:
            raise ValueError("h must be positive")
        n_points = int((xf - x0) / h) + 1
    
    if not isinstance(tolerance, (int, float)) or tolerance <= 0:
        raise ValueError("tolerance must be positive")
    
    # Apply integration method
    if method == 'euler':
        result = _euler_method(func, y0, x0, xf, h, adaptive, tolerance)
    elif method == 'modified_euler':
        result = _modified_euler_method(func, y0, x0, xf, h, adaptive, tolerance)
    elif method == 'runge_kutta_4':
        result = _runge_kutta_4_method(func, y0, x0, xf, h, adaptive, tolerance)
    elif method == 'runge_kutta_2':
        result = _runge_kutta_2_method(func, y0, x0, xf, h, adaptive, tolerance)
    elif method == 'midpoint':
        result = _midpoint_method(func, y0, x0, xf, h, adaptive, tolerance)
    elif method == 'adams_bashforth':
        result = _adams_bashforth_method(func, y0, x0, xf, h)
    
    result['method_used'] = method
    return result


def _euler_method(func: Callable, y0: float, x0: float, xf: float,
                 h: float, adaptive: bool, tolerance: float) -> Dict[str, Any]:
    """Forward Euler method implementation."""
    x_values = [x0]
    y_values = [y0]
    
    x = x0
    y = y0
    step_count = 0
    total_h = 0
    
    while x < xf:
        if adaptive:
            # Simple adaptive step control
            h1 = h
            y1 = y + h1 * func(x, y)
            
            h2 = h / 2
            y_temp = y + h2 * func(x, y)
            y2 = y_temp + h2 * func(x + h2, y_temp)
            
            error = abs(y2 - y1)
            
            if error < tolerance:
                # Accept step, possibly increase h
                if error < tolerance / 10:
                    h = min(h * 1.5, (xf - x) / 2)
                y = y1
                x += h1
                total_h += h1
            else:
                # Reduce step size
                h = h / 2
                continue
        else:
            # Fixed step
            if x + h > xf:
                h = xf - x
            y = y + h * func(x, y)
            x += h
            total_h += h
        
        x_values.append(x)
        y_values.append(y)
        step_count += 1
    
    avg_step = total_h / step_count if step_count > 0 else h
    
    return {
        'x': np.array(x_values),
        'y': np.array(y_values),
        'step_size': avg_step,
        'n_steps': step_count,
        'error_estimate': None
    }


def _modified_euler_method(func: Callable, y0: float, x0: float, xf: float,
                          h: float, adaptive: bool, tolerance: float) -> Dict[str, Any]:
    """Modified Euler (Heun's) method implementation."""
    x_values = [x0]
    y_values = [y0]
    
    x = x0
    y = y0
    step_count = 0
    total_h = 0
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        # Predictor step (Euler)
        k1 = func(x, y)
        y_pred = y + h * k1
        
        # Corrector step
        k2 = func(x + h, y_pred)
        y_new = y + h * (k1 + k2) / 2
        
        if adaptive:
            # Simple error estimate
            y_euler = y + h * k1
            error = abs(y_new - y_euler)
            
            if error < tolerance:
                y = y_new
                x += h
                total_h += h
                x_values.append(x)
                y_values.append(y)
                step_count += 1
                
                if error < tolerance / 10:
                    h = min(h * 1.2, (xf - x) / 2)
            else:
                h = h / 2
                continue
        else:
            y = y_new
            x += h
            total_h += h
            x_values.append(x)
            y_values.append(y)
            step_count += 1
    
    avg_step = total_h / step_count if step_count > 0 else h
    
    return {
        'x': np.array(x_values),
        'y': np.array(y_values),
        'step_size': avg_step,
        'n_steps': step_count,
        'error_estimate': None
    }


def _runge_kutta_4_method(func: Callable, y0: float, x0: float, xf: float,
                         h: float, adaptive: bool, tolerance: float) -> Dict[str, Any]:
    """Fourth-order Runge-Kutta method implementation."""
    x_values = [x0]
    y_values = [y0]
    
    x = x0
    y = y0
    step_count = 0
    total_h = 0
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        k1 = func(x, y)
        k2 = func(x + h/2, y + h*k1/2)
        k3 = func(x + h/2, y + h*k2/2)
        k4 = func(x + h, y + h*k3)
        
        y_new = y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
        
        if adaptive:
            # Embedded Runge-Kutta error estimate
            y_rk2 = y + h * (k1 + k4) / 2  # Simplified 2nd order
            error = abs(y_new - y_rk2) / 15  # Error estimate
            
            if error < tolerance:
                y = y_new
                x += h
                total_h += h
                x_values.append(x)
                y_values.append(y)
                step_count += 1
                
                if error < tolerance / 32:
                    h = min(h * 1.2, (xf - x) / 2)
            else:
                h = h / 2
                continue
        else:
            y = y_new
            x += h
            total_h += h
            x_values.append(x)
            y_values.append(y)
            step_count += 1
    
    avg_step = total_h / step_count if step_count > 0 else h
    
    return {
        'x': np.array(x_values),
        'y': np.array(y_values),
        'step_size': avg_step,
        'n_steps': step_count,
        'error_estimate': None
    }


def _runge_kutta_2_method(func: Callable, y0: float, x0: float, xf: float,
                         h: float, adaptive: bool, tolerance: float) -> Dict[str, Any]:
    """Second-order Runge-Kutta method implementation."""
    x_values = [x0]
    y_values = [y0]
    
    x = x0
    y = y0
    step_count = 0
    total_h = 0
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        k1 = func(x, y)
        k2 = func(x + h, y + h*k1)
        
        y_new = y + h * (k1 + k2) / 2
        
        if adaptive:
            # Compare with Euler step for error estimate
            y_euler = y + h * k1
            error = abs(y_new - y_euler)
            
            if error < tolerance:
                y = y_new
                x += h
                total_h += h
                x_values.append(x)
                y_values.append(y)
                step_count += 1
                
                if error < tolerance / 10:
                    h = min(h * 1.2, (xf - x) / 2)
            else:
                h = h / 2
                continue
        else:
            y = y_new
            x += h
            total_h += h
            x_values.append(x)
            y_values.append(y)
            step_count += 1
    
    avg_step = total_h / step_count if step_count > 0 else h
    
    return {
        'x': np.array(x_values),
        'y': np.array(y_values),
        'step_size': avg_step,
        'n_steps': step_count,
        'error_estimate': None
    }


def _midpoint_method(func: Callable, y0: float, x0: float, xf: float,
                    h: float, adaptive: bool, tolerance: float) -> Dict[str, Any]:
    """Midpoint method implementation."""
    x_values = [x0]
    y_values = [y0]
    
    x = x0
    y = y0
    step_count = 0
    total_h = 0
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        k1 = func(x, y)
        k2 = func(x + h/2, y + h*k1/2)
        
        y_new = y + h * k2
        
        if adaptive:
            # Compare with Euler for error estimate
            y_euler = y + h * k1
            error = abs(y_new - y_euler)
            
            if error < tolerance:
                y = y_new
                x += h
                total_h += h
                x_values.append(x)
                y_values.append(y)
                step_count += 1
                
                if error < tolerance / 10:
                    h = min(h * 1.2, (xf - x) / 2)
            else:
                h = h / 2
                continue
        else:
            y = y_new
            x += h
            total_h += h
            x_values.append(x)
            y_values.append(y)
            step_count += 1
    
    avg_step = total_h / step_count if step_count > 0 else h
    
    return {
        'x': np.array(x_values),
        'y': np.array(y_values),
        'step_size': avg_step,
        'n_steps': step_count,
        'error_estimate': None
    }


def _adams_bashforth_method(func: Callable, y0: float, x0: float, xf: float,
                           h: float) -> Dict[str, Any]:
    """Adams-Bashforth multi-step method implementation."""
    # Use RK4 for first few points
    x_values = [x0]
    y_values = [y0]
    f_values = [func(x0, y0)]
    
    x = x0
    y = y0
    
    # Generate first 3 points using RK4
    for i in range(3):
        if x >= xf:
            break
            
        if x + h > xf:
            h = xf - x
            
        k1 = func(x, y)
        k2 = func(x + h/2, y + h*k1/2)
        k3 = func(x + h/2, y + h*k2/2) 
        k4 = func(x + h, y + h*k3)
        
        y = y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
        x += h
        
        x_values.append(x)
        y_values.append(y)
        f_values.append(func(x, y))
    
    # Continue with Adams-Bashforth 4th order
    step_count = len(x_values) - 1
    
    while x < xf:
        if x + h > xf:
            h = xf - x
        
        if len(f_values) >= 4:
            # 4th order Adams-Bashforth
            y_new = y + h * (55*f_values[-1] - 59*f_values[-2] + 37*f_values[-3] - 9*f_values[-4]) / 24
        else:
            # Fall back to lower order
            y_new = y + h * f_values[-1]
        
        x += h
        y = y_new
        
        x_values.append(x)
        y_values.append(y)
        f_values.append(func(x, y))
        
        # Keep only last 4 function values for efficiency
        if len(f_values) > 4:
            f_values.pop(0)
        
        step_count += 1
    
    return {
        'x': np.array(x_values),
        'y': np.array(y_values),
        'step_size': h,
        'n_steps': step_count,
        'error_estimate': None
    }


__all__ = ['differential_equation_solver']
