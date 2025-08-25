"""
Test special functions module.
"""

import pytest
import math
from mathematical_functions.advanced.special_functions import special_functions


class TestSpecialFunctions:
    """Test cases for special functions."""
    
    def test_gamma_function_integers(self):
        """Test gamma function for integer values."""
        # Γ(1) = 0! = 1
        result = special_functions(1, 'gamma')
        assert abs(result['value'] - 1.0) < 1e-10
        
        # Γ(4) = 3! = 6
        result = special_functions(4, 'gamma')
        assert abs(result['value'] - 6.0) < 1e-6
    
    def test_gamma_function_half_integer(self):
        """Test gamma function for half-integer values."""
        # Γ(0.5) = √π
        result = special_functions(0.5, 'gamma')
        expected = math.sqrt(math.pi)
        assert abs(result['value'] - expected) < 1e-6
    
    def test_gamma_function_negative_values(self):
        """Test gamma function for negative values."""
        # Should work for non-integer negative values
        result = special_functions(-0.5, 'gamma')
        expected = -2 * math.sqrt(math.pi)
        assert abs(result['value'] - expected) < 1e-6
        
        # Should raise error for negative integers
        with pytest.raises(ValueError):
            special_functions(-1, 'gamma')
    
    def test_beta_function(self):
        """Test beta function."""
        # B(1,1) = 1
        result = special_functions(1, 'beta', n=1)
        assert abs(result['value'] - 1.0) < 1e-10
        
        # B(2,3) = Γ(2)Γ(3)/Γ(5) = 1*2/24 = 1/12
        result = special_functions(2, 'beta', n=3)
        expected = 1/12
        assert abs(result['value'] - expected) < 1e-10
    
    def test_error_function(self):
        """Test error function."""
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
    
    def test_complementary_error_function(self):
        """Test complementary error function."""
        # erfc(x) + erf(x) = 1
        x = 1.5
        erf_result = special_functions(x, 'erf')
        erfc_result = special_functions(x, 'erfc')
        assert abs(erf_result['value'] + erfc_result['value'] - 1.0) < 1e-10
    
    def test_bessel_j_function(self):
        """Test Bessel J function."""
        # J_0(0) = 1
        result = special_functions(0, 'bessel_j', n=0)
        assert abs(result['value'] - 1.0) < 1e-10
        
        # J_n(0) = 0 for n > 0
        result = special_functions(0, 'bessel_j', n=1)
        assert abs(result['value']) < 1e-10
    
    def test_modified_bessel_i_function(self):
        """Test Modified Bessel I function."""
        # I_0(0) = 1
        result = special_functions(0, 'modified_bessel_i', n=0)
        assert abs(result['value'] - 1.0) < 1e-10
        
        # I_n(0) = 0 for n > 0
        result = special_functions(0, 'modified_bessel_i', n=1)
        assert abs(result['value']) < 1e-10
    
    def test_elliptic_k_function(self):
        """Test complete elliptic integral K."""
        # K(0) = π/2
        result = special_functions(0, 'elliptic_k')
        expected = math.pi / 2
        assert abs(result['value'] - expected) < 1e-10
    
    def test_elliptic_e_function(self):
        """Test complete elliptic integral E."""
        # E(0) = π/2
        result = special_functions(0, 'elliptic_e')
        expected = math.pi / 2
        assert abs(result['value'] - expected) < 1e-10
        
        # E(1) = 1
        result = special_functions(1, 'elliptic_e')
        assert abs(result['value'] - 1.0) < 1e-6
    
    def test_zeta_function(self):
        """Test Riemann zeta function."""
        # ζ(2) = π²/6
        result = special_functions(2, 'zeta')
        expected = math.pi**2 / 6
        assert abs(result['value'] - expected) < 1e-3
        
        # Should raise error at s=1 (pole)
        with pytest.raises(ValueError):
            special_functions(1, 'zeta')
    
    def test_invalid_function_type(self):
        """Test invalid function type."""
        with pytest.raises(ValueError):
            special_functions(1, 'invalid_function')
    
    def test_missing_n_parameter(self):
        """Test missing n parameter for functions that require it."""
        with pytest.raises(ValueError):
            special_functions(1, 'beta')  # Missing n
        
        with pytest.raises(ValueError):
            special_functions(1, 'bessel_j')  # Missing n
    
    def test_convergence_info(self):
        """Test that convergence information is returned."""
        result = special_functions(2.5, 'gamma')
        assert 'convergence_info' in result
        assert 'terms_used' in result
        assert isinstance(result['terms_used'], int)
    
    def test_tolerance_parameter(self):
        """Test custom tolerance parameter."""
        result = special_functions(1.5, 'erf', tolerance=1e-6)
        assert result['value'] is not None
        
        # Different tolerance should potentially give different precision
        result_strict = special_functions(1.5, 'erf', tolerance=1e-12)
        assert result_strict['value'] is not None
    
    def test_max_terms_parameter(self):
        """Test max_terms parameter."""
        result = special_functions(1.5, 'erf', max_terms=50)
        assert result['terms_used'] <= 50


if __name__ == '__main__':
    pytest.main([__file__])
