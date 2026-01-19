import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from python_utils.testing_functions.assertion_helpers.assert_in_range import assert_in_range


def test_assert_in_range_value_in_range() -> None:
    """
    Test case 1: Assert value within range.
    """
    # Act & Assert
    assert_in_range(5, 1, 10)


def test_assert_in_range_value_at_min() -> None:
    """
    Test case 2: Assert value at minimum boundary.
    """
    # Act & Assert
    assert_in_range(1, 1, 10)


def test_assert_in_range_value_at_max() -> None:
    """
    Test case 3: Assert value at maximum boundary.
    """
    # Act & Assert
    assert_in_range(10, 1, 10)


def test_assert_in_range_same_min_max() -> None:
    """
    Test case 4: Assert value when min equals max.
    """
    # Act & Assert
    assert_in_range(5, 5, 5)


def test_assert_in_range_negative_range() -> None:
    """
    Test case 5: Assert value in negative range.
    """
    # Act & Assert
    assert_in_range(-5, -10, -1)


def test_assert_in_range_type_error_value() -> None:
    """
    Test case 6: TypeError for invalid value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="value must be a number"):
        assert_in_range("5", 1, 10)


def test_assert_in_range_type_error_min_value() -> None:
    """
    Test case 7: TypeError for invalid min_value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="min_value must be a number"):
        assert_in_range(5, "1", 10)


def test_assert_in_range_type_error_max_value() -> None:
    """
    Test case 8: TypeError for invalid max_value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="max_value must be a number"):
        assert_in_range(5, 1, "10")


def test_assert_in_range_value_error_min_greater_than_max() -> None:
    """
    Test case 9: ValueError when min_value > max_value.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="min_value .* must be <= max_value"):
        assert_in_range(5, 10, 1)


def test_assert_in_range_assertion_error_below_range() -> None:
    """
    Test case 10: AssertionError when value below range.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Value .* is not in range"):
        assert_in_range(0, 1, 10)


def test_assert_in_range_assertion_error_above_range() -> None:
    """
    Test case 11: AssertionError when value above range.
    """
    # Act & Assert
    with pytest.raises(AssertionError, match="Value .* is not in range"):
        assert_in_range(11, 1, 10)
