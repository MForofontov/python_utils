import pytest
import math
from mathematical_functions.advanced.special_functions import special_functions


def test_special_functions_gamma_integers() -> None:
    """
    Test case 1: Test gamma function for integer values.
    """
    # Γ(1) = 0! = 1
    result = special_functions(1, 'gamma')
    assert abs(result['value'] - 1.0) < 1e-10
    
    # Γ(4) = 3! = 6
    result = special_functions(4, 'gamma')
    assert abs(result['value'] - 6.0) < 1e-6


def test_special_functions_gamma_half_integer() -> None:
    """
    Test case 2: Test gamma function for half-integer values.
    """
    # Γ(0.5) = √π
    result = special_functions(0.5, 'gamma')
    expected = math.sqrt(math.pi)
    assert abs(result['value'] - expected) < 1e-6


def test_special_functions_gamma_negative_values() -> None:
    """
    Test case 3: Test gamma function for negative values.
    """
    # Should work for non-integer negative values
    result = special_functions(-0.5, 'gamma')
    expected = -2 * math.sqrt(math.pi)
    assert abs(result['value'] - expected) < 1e-6
    
    # Should raise error for negative integers
    with pytest.raises(ValueError):
        special_functions(-1, 'gamma')


def test_special_functions_beta_function() -> None:
    """
    Test case 4: Test beta function.
    """
    # B(1,1) = 1
    result = special_functions(1, 'beta', n=1)
    assert abs(result['value'] - 1.0) < 1e-10
    
    # B(2,3) = Γ(2)Γ(3)/Γ(5) = 1*2/24 = 1/12
    result = special_functions(2, 'beta', n=3)
    expected = 1/12
    assert abs(result['value'] - expected) < 1e-10


def test_special_functions_error_function() -> None:
    """
    Test case 5: Test error function.
    """
    # erf(0) = 0
    result = special_functions(0, 'erf')
    assert abs(result['value']) < 1e-10
    
    # erf(∞) ≈ 1, test with large value
    result = special_functions(3.0, 'erf')
    assert result['value'] > 0.99
    
    # erf(-x) = -erf(x)
    result_pos = special_functions(1.0, 'erf')
    result_neg = special_functions(-1.0, 'erf')
    assert abs(result_pos['value'] + result_neg['value']) < 1e-10


def test_special_functions_complementary_error_function() -> None:
    """
    Test case 6: Test complementary error function.
    """
    # erfc(x) + erf(x) = 1
    x = 1.5
    erf_result = special_functions(x, 'erf')
    erfc_result = special_functions(x, 'erfc')
    assert abs(erf_result['value'] + erfc_result['value'] - 1.0) < 1e-10


def test_special_functions_bessel_j_function() -> None:
    """
    Test case 7: Test Bessel J function.
    """
    # J_0(0) = 1
    result = special_functions(0, 'bessel_j', n=0)
    assert abs(result['value'] - 1.0) < 1e-10
    
    # J_n(0) = 0 for n > 0
    result = special_functions(0, 'bessel_j', n=1)
    assert abs(result['value']) < 1e-10


def test_special_functions_modified_bessel_i_function() -> None:
    """
    Test case 8: Test Modified Bessel I function.
    """
    # I_0(0) = 1
    result = special_functions(0, 'modified_bessel_i', n=0)
    assert abs(result['value'] - 1.0) < 1e-10
    
    # I_n(0) = 0 for n > 0
    result = special_functions(0, 'modified_bessel_i', n=1)
    assert abs(result['value']) < 1e-10


def test_special_functions_elliptic_k_function() -> None:
    """
    Test case 9: Test complete elliptic integral K.
    """
    # K(0) = π/2
    result = special_functions(0, 'elliptic_k')
    expected = math.pi / 2
    assert abs(result['value'] - expected) < 1e-10


def test_special_functions_elliptic_e_function() -> None:
    """
    Test case 10: Test complete elliptic integral E.
    """
    # E(0) = π/2
    result = special_functions(0, 'elliptic_e')
    expected = math.pi / 2
    assert abs(result['value'] - expected) < 1e-10
    
    # E(1) = 1
    result = special_functions(1, 'elliptic_e')
    assert abs(result['value'] - 1.0) < 1e-6


def test_special_functions_zeta_function() -> None:
    """
    Test case 11: Test Riemann zeta function.
    """
    # ζ(2) = π²/6
    result = special_functions(2, 'zeta')
    expected = math.pi**2 / 6
    assert abs(result['value'] - expected) < 1e-3
    
    # Should raise error at s=1 (pole)
    with pytest.raises(ValueError):
        special_functions(1, 'zeta')


def test_special_functions_invalid_function_type() -> None:
    """
    Test case 12: Test invalid function type.
    """
    with pytest.raises(ValueError):
        special_functions(1, 'invalid_function')


def test_special_functions_missing_n_parameter() -> None:
    """
    Test case 13: Test missing n parameter for functions that require it.
    """
    with pytest.raises(ValueError):
        special_functions(1, 'beta')  # Missing n
    
    with pytest.raises(ValueError):
        special_functions(1, 'bessel_j')  # Missing n


def test_special_functions_convergence_info() -> None:
    """
    Test case 14: Test that convergence information is returned.
    """
    result = special_functions(2.5, 'gamma')
    assert 'convergence_info' in result
    assert 'terms_used' in result
    assert isinstance(result['terms_used'], int)


def test_special_functions_tolerance_parameter() -> None:
    """
    Test case 15: Test custom tolerance parameter.
    """
    result = special_functions(1.5, 'erf', tolerance=1e-6)
    assert result['value'] is not None
    
    # Different tolerance should potentially give different precision
    result_strict = special_functions(1.5, 'erf', tolerance=1e-12)
    assert result_strict['value'] is not None


def test_special_functions_max_terms_parameter() -> None:
    """
    Test case 16: Test max_terms parameter.
    """
    result = special_functions(1.5, 'erf', max_terms=50)
    assert result['terms_used'] <= 50


def test_special_functions_type_errors() -> None:
    """
    Test case 17: Test type error handling.
    """
    with pytest.raises(TypeError, match="x must be numeric"):
        special_functions("invalid", 'gamma')
    
    with pytest.raises(TypeError, match="function_type must be string"):
        special_functions(1, 123)


def test_special_functions_invalid_parameters() -> None:
    """
    Test case 18: Test invalid parameter values.
    """
    with pytest.raises(ValueError, match="tolerance must be positive"):
        special_functions(1.5, 'erf', tolerance=0)
    
    with pytest.raises(ValueError, match="max_terms must be positive integer"):
        special_functions(1.5, 'erf', max_terms=0)


def test_special_functions_bessel_y_positive_x() -> None:
    """
    Test case 19: Test Bessel Y function with positive x.
    """
    result = special_functions(1.0, 'bessel_y', n=0)
    assert isinstance(result['value'], (int, float))
    
    # Should raise error for x <= 0
    with pytest.raises(ValueError):
        special_functions(0, 'bessel_y', n=0)


def test_special_functions_modified_bessel_k_positive_x() -> None:
    """
    Test case 20: Test Modified Bessel K function with positive x.
    """
    result = special_functions(1.0, 'modified_bessel_k', n=0)
    assert isinstance(result['value'], (int, float))
    assert result['value'] >= 0  # K_n(x) >= 0
    
    # Should raise error for x <= 0
    with pytest.raises(ValueError):
        special_functions(0, 'modified_bessel_k', n=0)


def test_special_functions_elliptic_invalid_parameter() -> None:
    """
    Test case 21: Test elliptic functions with invalid parameters.
    """
    # K(m) undefined for m >= 1
    with pytest.raises(ValueError):
        special_functions(1.5, 'elliptic_k')
    
    # E(m) undefined for m > 1
    with pytest.raises(ValueError):
        special_functions(1.5, 'elliptic_e')


def test_special_functions_digamma_function() -> None:
    """
    Test case 22: Test digamma function.
    """
    result = special_functions(1.0, 'digamma')
    assert isinstance(result['value'], (int, float))
    
    # Should raise error for non-positive integers
    with pytest.raises(ValueError):
        special_functions(-1, 'digamma')
