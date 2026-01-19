import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from testing_functions.assertion_helpers.assert_almost_equal import (
    assert_almost_equal,
)


def test_assert_almost_equal_exactly_equal() -> None:
    """
    Test case 1: Assert exactly equal values.
    """
    # Act & Assert
    assert_almost_equal(1.0, 1.0)


def test_assert_almost_equal_within_tolerance() -> None:
    """
    Test case 2: Assert values within tolerance.
    """
    # Act & Assert
    assert_almost_equal(0.1 + 0.2, 0.3, 1e-9)


def test_assert_almost_equal_custom_tolerance() -> None:
    """
    Test case 4: Assert values with custom tolerance.
    """
    # Act & Assert
    assert_almost_equal(1.001, 1.002, 0.01)


def test_assert_almost_equal_integers() -> None:
    """
    Test case 5: Assert with integer values.
    """
    # Act & Assert
    assert_almost_equal(5, 5)


def test_assert_almost_equal_type_error_actual() -> None:
    """
    Test case 6: TypeError for invalid actual type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="actual must be a number"):
        assert_almost_equal("1.0", 1.0)


def test_assert_almost_equal_type_error_expected() -> None:
    """
    Test case 7: TypeError for invalid expected type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="expected must be a number"):
        assert_almost_equal(1.0, "1.0")


def test_assert_almost_equal_type_error_tolerance() -> None:
    """
    Test case 8: TypeError for invalid tolerance type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="tolerance must be a number"):
        assert_almost_equal(1.0, 1.0, "0.1")


def test_assert_almost_equal_value_error_negative_tolerance() -> None:
    """
    Test case 9: ValueError for negative tolerance.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="tolerance must be non-negative"):
        assert_almost_equal(1.0, 1.0, -0.1)


def test_assert_almost_equal_assertion_error_exceeds_tolerance() -> None:
    """
    Test case 10: AssertionError when difference exceeds tolerance.
    """
    # Act & Assert
    with pytest.raises(
        AssertionError, match="Values differ by .* which exceeds tolerance"
    ):
        assert_almost_equal(1.0, 2.0, 0.1)
