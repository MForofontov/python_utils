"""
Special mathematical functions and constants.

This module provides implementations of special functions commonly used
in mathematics, physics, and engineering applications.
"""

import math
from typing import Union, Dict, Any, List, Optional


def special_functions(x: Union[float, int],
                     function_type: str = 'gamma',
                     n: Optional[int] = None,
                     **kwargs) -> Dict[str, Any]:
    """
    Compute various special mathematical functions.

    Evaluates special functions including gamma, beta, error functions,
    Bessel functions, and others at given points.

    Parameters
    ----------
    x : float or int
        Input value at which to evaluate the function.
    function_type : str, optional
        Type of special function. Options:
        - 'gamma': Gamma function Γ(x) (default)
        - 'beta': Beta function B(x,n) (requires n parameter)
        - 'digamma': Digamma function ψ(x)
        - 'erf': Error function erf(x)
        - 'erfc': Complementary error function erfc(x)
        - 'bessel_j': Bessel function of first kind J_n(x) (requires n)
        - 'bessel_y': Bessel function of second kind Y_n(x) (requires n)
        - 'modified_bessel_i': Modified Bessel function I_n(x) (requires n)
        - 'modified_bessel_k': Modified Bessel function K_n(x) (requires n)
        - 'elliptic_k': Complete elliptic integral of first kind K(x)
        - 'elliptic_e': Complete elliptic integral of second kind E(x)
        - 'zeta': Riemann zeta function ζ(x)
    n : int, optional
        Order parameter for functions requiring it (e.g., Bessel functions).
    **kwargs : dict
        Additional parameters:
        - tolerance : float, convergence tolerance (default: 1e-10)
        - max_terms : int, maximum series terms (default: 1000)

    Returns
    -------
    dict
        Dictionary containing:
        - 'value': Function value at x
        - 'function_type': Function type evaluated
        - 'convergence_info': Information about series convergence
        - 'terms_used': Number of terms used in series expansion

    Raises
    ------
    TypeError
        If inputs are not of correct types.
    ValueError
        If parameters are invalid or function undefined at x.

    Examples
    --------
    >>> # Gamma function: Γ(4) = 3! = 6
    >>> result = special_functions(4, 'gamma')
    >>> abs(result['value'] - 6.0) < 1e-10
    True
    
    >>> # Error function: erf(0) = 0
    >>> result = special_functions(0, 'erf')
    >>> abs(result['value']) < 1e-10
    True

    Notes
    -----
    Many special functions are computed using series expansions or
    continued fractions. Convergence depends on the input value and
    may require different algorithms for different ranges.
    """
    # Input validation
    if not isinstance(x, (int, float)):
        raise TypeError("x must be numeric")
    if not isinstance(function_type, str):
        raise TypeError("function_type must be string")
    
    function_type = function_type.lower()
    tolerance = kwargs.get('tolerance', 1e-10)
    max_terms = kwargs.get('max_terms', 1000)
    
    valid_functions = ['gamma', 'beta', 'digamma', 'erf', 'erfc', 'bessel_j', 
                      'bessel_y', 'modified_bessel_i', 'modified_bessel_k',
                      'elliptic_k', 'elliptic_e', 'zeta']
    
    if function_type not in valid_functions:
        raise ValueError(f"function_type must be one of {valid_functions}")
    
    # Validate tolerance and max_terms
    if not isinstance(tolerance, (int, float)) or tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if not isinstance(max_terms, int) or max_terms <= 0:
        raise ValueError("max_terms must be positive integer")
    
    # Apply function
    if function_type == 'gamma':
        result = _gamma_function(x, tolerance, max_terms)
    elif function_type == 'beta':
        if n is None:
            raise ValueError("beta function requires n parameter")
        result = _beta_function(x, n, tolerance, max_terms)
    elif function_type == 'digamma':
        result = _digamma_function(x, tolerance, max_terms)
    elif function_type == 'erf':
        result = _error_function(x, tolerance, max_terms)
    elif function_type == 'erfc':
        result = _complementary_error_function(x, tolerance, max_terms)
    elif function_type == 'bessel_j':
        if n is None:
            raise ValueError("bessel_j function requires n parameter")
        result = _bessel_j_function(n, x, tolerance, max_terms)
    elif function_type == 'bessel_y':
        if n is None:
            raise ValueError("bessel_y function requires n parameter")
        result = _bessel_y_function(n, x, tolerance, max_terms)
    elif function_type == 'modified_bessel_i':
        if n is None:
            raise ValueError("modified_bessel_i function requires n parameter")
        result = _modified_bessel_i_function(n, x, tolerance, max_terms)
    elif function_type == 'modified_bessel_k':
        if n is None:
            raise ValueError("modified_bessel_k function requires n parameter")
        result = _modified_bessel_k_function(n, x, tolerance, max_terms)
    elif function_type == 'elliptic_k':
        result = _elliptic_k_function(x, tolerance, max_terms)
    elif function_type == 'elliptic_e':
        result = _elliptic_e_function(x, tolerance, max_terms)
    elif function_type == 'zeta':
        result = _zeta_function(x, tolerance, max_terms)
    
    result['function_type'] = function_type
    return result


def _gamma_function(x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Gamma function using Lanczos approximation."""
    if x <= 0 and x == int(x):
        raise ValueError("Gamma function undefined for non-positive integers")
    
    # Lanczos coefficients (g=7, n=9)
    g = 7
    coeff = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
             771.32342877765313, -176.61502916214059, 12.507343278686905,
             -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
    
    if x < 0.5:
        # Use reflection formula: Γ(z)Γ(1-z) = π/sin(πz)
        result = math.pi / (math.sin(math.pi * x) * _gamma_function(1 - x, tolerance, max_terms)['value'])
        return {
            'value': result,
            'convergence_info': 'Used reflection formula',
            'terms_used': 1
        }
    
    x -= 1
    a = coeff[0]
    for i in range(1, len(coeff)):
        a += coeff[i] / (x + i)
    
    t = x + g + 0.5
    result = math.sqrt(2 * math.pi) * (t ** (x + 0.5)) * math.exp(-t) * a
    
    return {
        'value': result,
        'convergence_info': 'Lanczos approximation converged',
        'terms_used': len(coeff)
    }


def _beta_function(x: float, y: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Beta function using Gamma function relation: B(x,y) = Γ(x)Γ(y)/Γ(x+y)."""
    try:
        gamma_x = _gamma_function(x, tolerance, max_terms)['value']
        gamma_y = _gamma_function(y, tolerance, max_terms)['value']
        gamma_xy = _gamma_function(x + y, tolerance, max_terms)['value']
        
        result = gamma_x * gamma_y / gamma_xy
        
        return {
            'value': result,
            'convergence_info': 'Computed using Gamma function relation',
            'terms_used': 3
        }
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Beta function undefined for given parameters: {e}")


def _digamma_function(x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Digamma function using series expansion."""
    if x <= 0 and x == int(x):
        raise ValueError("Digamma function undefined for non-positive integers")
    
    # For large x, use asymptotic expansion
    if x > 6:
        result = math.log(x) - 1/(2*x)
        x_sq = x * x
        result -= 1/(12*x_sq) - 1/(120*x_sq*x_sq) + 1/(252*x_sq*x_sq*x_sq)
        
        return {
            'value': result,
            'convergence_info': 'Asymptotic expansion used',
            'terms_used': 4
        }
    
    # Use recurrence relation to shift to larger value
    original_x = x
    shift_count = 0
    while x <= 6:
        x += 1
        shift_count += 1
    
    # Compute for shifted value
    digamma_shifted = _digamma_function(x, tolerance, max_terms)['value']
    
    # Apply recurrence relation backward
    result = digamma_shifted
    for i in range(shift_count):
        result -= 1 / (x - 1 - i)
    
    return {
        'value': result,
        'convergence_info': f'Used recurrence relation with {shift_count} shifts',
        'terms_used': shift_count + 4
    }


def _error_function(x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Error function using series expansion."""
    if abs(x) > 2.5:
        # Use continued fraction for large |x|
        return _error_function_continued_fraction(x, tolerance, max_terms)
    
    # Series expansion: erf(x) = (2/√π) * Σ((-1)^n * x^(2n+1) / (n!(2n+1)))
    sqrt_pi = math.sqrt(math.pi)
    sum_val = 0
    term = x
    
    for n in range(max_terms):
        sum_val += term
        
        if abs(term) < tolerance:
            break
        
        # Next term: multiply by -x²/(n+1)
        term *= -x * x / (n + 1)
        term /= (2 * n + 3)
    
    result = 2 * sum_val / sqrt_pi
    
    return {
        'value': result,
        'convergence_info': 'Series expansion converged' if abs(term) < tolerance else 'Max terms reached',
        'terms_used': n + 1
    }


def _error_function_continued_fraction(x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Error function using continued fraction for large |x|."""
    # erfc(x) = (e^(-x²)/√π) * continued_fraction
    if x < 0:
        pos_result = _error_function_continued_fraction(-x, tolerance, max_terms)
        return {
            'value': -pos_result['value'],
            'convergence_info': pos_result['convergence_info'],
            'terms_used': pos_result['terms_used']
        }
    
    # Continued fraction approximation for erfc
    sqrt_pi = math.sqrt(math.pi)
    exp_factor = math.exp(-x * x)
    
    # Simple approximation for large x
    if x > 5:
        erfc_val = exp_factor / (sqrt_pi * x)
        erf_val = 1 - erfc_val
    else:
        # Use series for moderate x
        series_result = _error_function(x, tolerance, max_terms)
        erf_val = series_result['value']
    
    return {
        'value': erf_val,
        'convergence_info': 'Large argument approximation',
        'terms_used': 1
    }


def _complementary_error_function(x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Complementary Error function: erfc(x) = 1 - erf(x)."""
    erf_result = _error_function(x, tolerance, max_terms)
    
    return {
        'value': 1 - erf_result['value'],
        'convergence_info': erf_result['convergence_info'],
        'terms_used': erf_result['terms_used']
    }


def _bessel_j_function(n: int, x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Bessel function of first kind J_n(x) using series expansion."""
    if not isinstance(n, int):
        raise TypeError("n must be integer for Bessel functions")
    
    if x == 0:
        return {
            'value': 1.0 if n == 0 else 0.0,
            'convergence_info': 'Special case x=0',
            'terms_used': 1
        }
    
    # Series expansion: J_n(x) = (x/2)^n * Σ((-1)^k * (x/2)^(2k) / (k! * (n+k)!))
    x_half = x / 2
    sum_val = 0
    term = (x_half ** n) / math.factorial(n)
    
    for k in range(max_terms):
        sum_val += term
        
        if abs(term) < tolerance:
            break
        
        # Next term
        term *= -(x_half * x_half) / ((k + 1) * (n + k + 1))
    
    return {
        'value': sum_val,
        'convergence_info': 'Series expansion converged' if abs(term) < tolerance else 'Max terms reached',
        'terms_used': k + 1
    }


def _bessel_y_function(n: int, x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Bessel function of second kind Y_n(x) using approximation."""
    if x <= 0:
        raise ValueError("Bessel Y function undefined for x <= 0")
    
    # For small x, Y_n(x) has logarithmic singularity
    # Simple approximation for Y_0(x)
    if n == 0:
        if x < 2:
            result = (2/math.pi) * (math.log(x/2) + 0.5772156649)  # Euler's gamma
        else:
            # Asymptotic approximation for large x
            result = math.sqrt(2/(math.pi*x)) * math.sin(x - math.pi/4)
    else:
        # Higher order approximation
        if x < 2:
            result = -(math.factorial(n-1)/math.pi) * (2/x)**n
        else:
            result = math.sqrt(2/(math.pi*x)) * math.sin(x - n*math.pi/2 - math.pi/4)
    
    return {
        'value': result,
        'convergence_info': 'Approximation formula used',
        'terms_used': 1
    }


def _modified_bessel_i_function(n: int, x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Modified Bessel function I_n(x) using series expansion."""
    if x == 0:
        return {
            'value': 1.0 if n == 0 else 0.0,
            'convergence_info': 'Special case x=0',
            'terms_used': 1
        }
    
    # Series expansion: I_n(x) = (x/2)^n * Σ((x/2)^(2k) / (k! * (n+k)!))
    x_half = x / 2
    sum_val = 0
    term = (x_half ** abs(n)) / math.factorial(abs(n))
    
    for k in range(max_terms):
        sum_val += term
        
        if abs(term) < tolerance:
            break
        
        # Next term
        term *= (x_half * x_half) / ((k + 1) * (abs(n) + k + 1))
    
    return {
        'value': sum_val,
        'convergence_info': 'Series expansion converged' if abs(term) < tolerance else 'Max terms reached',
        'terms_used': k + 1
    }


def _modified_bessel_k_function(n: int, x: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Modified Bessel function K_n(x) using approximation."""
    if x <= 0:
        raise ValueError("Modified Bessel K function undefined for x <= 0")
    
    # Asymptotic approximation for large x
    if x > 2:
        result = math.sqrt(math.pi/(2*x)) * math.exp(-x)
    else:
        # For small x, use relation with I_n
        if n == 0:
            result = -math.log(x/2) - 0.5772156649  # Euler's gamma
        else:
            result = 0.5 * math.factorial(abs(n)-1) * (2/x)**abs(n)
    
    return {
        'value': max(0, result),  # K_n(x) >= 0
        'convergence_info': 'Approximation formula used',
        'terms_used': 1
    }


def _elliptic_k_function(m: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Complete Elliptic Integral of first kind K(m)."""
    if m >= 1:
        raise ValueError("Elliptic K function undefined for m >= 1")
    
    if abs(m) < tolerance:
        return {
            'value': math.pi / 2,
            'convergence_info': 'Special case m=0',
            'terms_used': 1
        }
    
    # Use arithmetic-geometric mean
    a = 1.0
    g = math.sqrt(1 - m)
    
    for k in range(max_terms):
        if abs(a - g) < tolerance:
            break
        
        a_new = (a + g) / 2
        g = math.sqrt(a * g)
        a = a_new
    
    result = math.pi / (2 * a)
    
    return {
        'value': result,
        'convergence_info': 'Arithmetic-geometric mean converged' if abs(a - g) < tolerance else 'Max terms reached',
        'terms_used': k + 1
    }


def _elliptic_e_function(m: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Complete Elliptic Integral of second kind E(m)."""
    if m > 1:
        raise ValueError("Elliptic E function undefined for m > 1")
    
    if abs(m) < tolerance:
        return {
            'value': math.pi / 2,
            'convergence_info': 'Special case m=0',
            'terms_used': 1
        }
    
    if abs(m - 1) < tolerance:
        return {
            'value': 1.0,
            'convergence_info': 'Special case m=1',
            'terms_used': 1
        }
    
    # Use series expansion
    result = math.pi / 2
    term = math.pi / 2 * m / 4
    
    for n in range(1, max_terms):
        result -= term
        
        if abs(term) < tolerance:
            break
        
        # Next term
        term *= m * (2*n - 1) * (2*n - 1) / (4 * n * (2*n + 1))
    
    return {
        'value': result,
        'convergence_info': 'Series expansion converged' if abs(term) < tolerance else 'Max terms reached',
        'terms_used': n + 1
    }


def _zeta_function(s: float, tolerance: float, max_terms: int) -> Dict[str, Any]:
    """Compute Riemann Zeta function ζ(s) using series expansion."""
    if abs(s - 1) < tolerance:
        raise ValueError("Zeta function has pole at s=1")
    
    if s < 0:
        raise ValueError("Zeta function implementation limited to s > 0")
    
    if s > 10:
        # For large s, zeta(s) ≈ 1
        return {
            'value': 1.0,
            'convergence_info': 'Large s approximation',
            'terms_used': 1
        }
    
    # Series expansion: ζ(s) = Σ(1/n^s) for n=1 to ∞
    sum_val = 0
    
    for n in range(1, max_terms + 1):
        term = 1 / (n ** s)
        sum_val += term
        
        if term < tolerance:
            break
    
    return {
        'value': sum_val,
        'convergence_info': 'Series expansion converged' if term < tolerance else 'Max terms reached',
        'terms_used': n
    }


__all__ = ['special_functions']
