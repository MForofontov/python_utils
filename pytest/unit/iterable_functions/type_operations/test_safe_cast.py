"""Unit tests for safe_cast and is_numeric functions."""
import pytest

from iterable_functions.type_operations.safe_cast import is_numeric, safe_cast


def test_safe_cast_string_to_int() -> None:
    """
    Test case 1: Cast string to integer.
    """
    # Act
    result = safe_cast("123", int)

    # Assert
    assert result == 123
    assert isinstance(result, int)


def test_safe_cast_string_to_int_with_default() -> None:
    """
    Test case 2: Failed cast returns default value.
    """
    # Act
    result = safe_cast("abc", int, 0)

    # Assert
    assert result == 0


def test_safe_cast_string_to_int_no_default() -> None:
    """
    Test case 3: Failed cast without default returns original value.
    """
    # Act
    result = safe_cast("abc", int)

    # Assert
    assert result == "abc"


def test_safe_cast_int_to_string() -> None:
    """
    Test case 4: Cast integer to string.
    """
    # Act
    result = safe_cast(42, str)

    # Assert
    assert result == "42"
    assert isinstance(result, str)


def test_safe_cast_float_to_int() -> None:
    """
    Test case 5: Cast float to integer.
    """
    # Act
    result = safe_cast(3.14, int)

    # Assert
    assert result == 3
    assert isinstance(result, int)


def test_safe_cast_string_to_float() -> None:
    """
    Test case 6: Cast string to float.
    """
    # Act
    result = safe_cast("3.14", float)

    # Assert
    assert result == 3.14
    assert isinstance(result, float)


def test_safe_cast_none_with_default() -> None:
    """
    Test case 7: None value with default returns default.
    """
    # Act
    result = safe_cast(None, str, "default")

    # Assert
    assert result == "default"


def test_safe_cast_none_without_default() -> None:
    """
    Test case 8: None value without default returns None.
    """
    # Act
    result = safe_cast(None, str)

    # Assert
    assert result is None


def test_safe_cast_string_to_bool_true() -> None:
    """
    Test case 9: Cast string to boolean (true values).
    """
    # Arrange
    true_values = ["true", "True", "TRUE", "1", "yes", "Yes", "on", "ON"]

    # Act & Assert
    for value in true_values:
        result = safe_cast(value, bool)
        assert result is True, f"Failed for value: {value}"


def test_safe_cast_string_to_bool_false() -> None:
    """
    Test case 10: Cast string to boolean (false values).
    """
    # Arrange
    false_values = ["false", "False", "FALSE", "0", "no", "No", "off", "OFF", ""]

    # Act & Assert
    for value in false_values:
        result = safe_cast(value, bool)
        assert result is False, f"Failed for value: {value}"


def test_safe_cast_string_to_bool_invalid() -> None:
    """
    Test case 11: Invalid string for bool returns default.
    """
    # Act
    result = safe_cast("maybe", bool, False)

    # Assert
    assert result is False


def test_safe_cast_number_to_bool() -> None:
    """
    Test case 12: Cast number to boolean.
    """
    # Act
    result_zero = safe_cast(0, bool)
    result_nonzero = safe_cast(5, bool)

    # Assert
    assert result_zero is False
    assert result_nonzero is True


def test_safe_cast_list_to_tuple() -> None:
    """
    Test case 13: Cast list to tuple.
    """
    # Act
    result = safe_cast([1, 2, 3], tuple)

    # Assert
    assert result == (1, 2, 3)
    assert isinstance(result, tuple)


def test_safe_cast_tuple_to_list() -> None:
    """
    Test case 14: Cast tuple to list.
    """
    # Act
    result = safe_cast((1, 2, 3), list)

    # Assert
    assert result == [1, 2, 3]
    assert isinstance(result, list)


def test_safe_cast_scalar_to_list() -> None:
    """
    Test case 15: Cast scalar value to list.
    """
    # Act
    result = safe_cast(42, list)

    # Assert
    assert result == [42]


def test_safe_cast_string_with_decimal_to_int() -> None:
    """
    Test case 16: Cast string with decimal to int.
    """
    # Act
    result = safe_cast("3.14", int)

    # Assert
    assert result == 3
    assert isinstance(result, int)


def test_safe_cast_type_error_non_type() -> None:
    """
    Test case 17: TypeError when target_type is not a type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="target_type must be a type"):
        safe_cast("123", "not a type")  # type: ignore


def test_is_numeric_with_int() -> None:
    """
    Test case 18: is_numeric returns True for integers.
    """
    # Act
    result = is_numeric(42)

    # Assert
    assert result is True


def test_is_numeric_with_float() -> None:
    """
    Test case 19: is_numeric returns True for floats.
    """
    # Act
    result = is_numeric(3.14)

    # Assert
    assert result is True


def test_is_numeric_with_complex() -> None:
    """
    Test case 20: is_numeric returns True for complex numbers.
    """
    # Act
    result = is_numeric(1 + 2j)

    # Assert
    assert result is True


def test_is_numeric_with_string() -> None:
    """
    Test case 21: is_numeric returns False for strings.
    """
    # Act
    result = is_numeric("123")

    # Assert
    assert result is False


def test_is_numeric_with_none() -> None:
    """
    Test case 22: is_numeric returns False for None.
    """
    # Act
    result = is_numeric(None)

    # Assert
    assert result is False


def test_is_numeric_with_bool() -> None:
    """
    Test case 23: is_numeric returns False for booleans.
    """
    # Act
    result = is_numeric(True)

    # Assert
    assert result is False


def test_safe_cast_empty_string_to_int() -> None:
    """
    Test case 24: Empty string to int with default.
    """
    # Act
    result = safe_cast("", int, 0)

    # Assert
    assert result == 0


def test_safe_cast_preserves_original_on_failure() -> None:
    """
    Test case 25: Failed cast without default preserves original value.
    """
    # Arrange
    original = {"key": "value"}

    # Act
    result = safe_cast(original, int)

    # Assert
    assert result == original
    assert result is original
