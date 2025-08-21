import pytest
from statistics_functions.modes_within_value import modes_within_value


def test_difference_within_tolerance() -> None:
    """
    Test when the difference between modes is within the allowed tolerance.
    """
    # Test case 1: Difference within tolerance
    assert (
        modes_within_value(10, 12, 0.2) == True
    ), "Failed when difference is within tolerance"


def test_difference_exceeds_tolerance() -> None:
    """
    Test when the difference between modes exceeds the allowed tolerance.
    """
    # Test case 2: Difference exceeds tolerance
    assert (
        modes_within_value(10, 15, 0.2) == False
    ), "Failed when difference exceeds tolerance"


def test_equal_modes() -> None:
    """
    Test when both modes are equal.
    """
    # Test case 3: Equal modes
    assert (
        modes_within_value(10, 10, 0.2) == True
    ), "Failed when modes are equal"


def test_negative_modes() -> None:
    """
    Test support for negative mode values.
    """
    # Test case 4: Negative modes
    assert (
        modes_within_value(-10, -12, 0.2) == True
    ), "Failed with negative mode values"


def test_zero_tolerance() -> None:
    """
    Test when tolerance value is zero.
    """
    # Test case 5: Zero tolerance
    assert (
        modes_within_value(10, 10, 0.0) == True
    ), "Failed with zero tolerance"


def test_negative_value_raises_value_error() -> None:
    """
    Test that a negative tolerance value raises ValueError.
    """
    # Test case 6: Negative tolerance
    with pytest.raises(ValueError):
        modes_within_value(10, 12, -0.1)


def test_non_numeric_inputs_raise_type_error() -> None:
    """
    Test that non-numeric inputs raise TypeError.
    """
    # Test case 7: Non-numeric inputs
    with pytest.raises(TypeError):
        modes_within_value("a", 12, 0.2)

