import pytest

pytestmark = [pytest.mark.unit, pytest.mark.mathematical_functions]
from python_utils.mathematical_functions.basic.power import power


def test_power_positive_integers() -> None:
    """
    Test case 1: Test power with positive integers.
    """
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(10, 0) == 1


def test_power_negative_base() -> None:
    """
    Test case 2: Test power with negative base.
    """
    assert power(-2, 3) == -8
    assert power(-3, 2) == 9
    assert power(-1, 10) == 1


def test_power_negative_exponent() -> None:
    """
    Test case 3: Test power with negative exponent.
    """
    assert power(2, -1) == 0.5
    assert power(4, -2) == 0.0625
    assert power(10, -3) == 0.001


def test_power_float_values() -> None:
    """
    Test case 4: Test power with floating-point values.
    """
    assert power(2.5, 2) == 6.25
    assert power(9, 0.5) == 3.0
    assert abs(power(2.0, 3.0) - 8.0) < 1e-10


def test_power_zero_base() -> None:
    """
    Test case 5: Test power with zero base.
    """
    assert power(0, 5) == 0
    assert power(0, 1) == 0
    # Note: 0^0 is 1 in Python


def test_power_one_base() -> None:
    """
    Test case 6: Test power with base = 1.
    """
    assert power(1, 100) == 1
    assert power(1, -5) == 1
    assert power(1, 0) == 1


def test_power_fractional_exponent() -> None:
    """
    Test case 7: Test power with fractional exponent.
    """
    assert power(16, 0.25) == 2.0
    assert power(27, 1 / 3) == 3.0


def test_power_type_error_base() -> None:
    """
    Test case 8: Test power with invalid type for base.
    """
    with pytest.raises(TypeError, match="base must be numeric"):
        power("2", 3)


def test_power_type_error_exponent() -> None:
    """
    Test case 9: Test power with invalid type for exponent.
    """
    with pytest.raises(TypeError, match="exponent must be numeric"):
        power(2, "3")
