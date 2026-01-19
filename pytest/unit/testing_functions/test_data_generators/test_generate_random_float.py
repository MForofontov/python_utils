import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from testing_functions.test_data_generators.generate_random_float import (
    generate_random_float,
)


def test_generate_random_float_default_parameters() -> None:
    """
    Test case 1: Generate random float with default parameters.
    """
    # Act
    result = generate_random_float()

    # Assert
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


def test_generate_random_float_custom_range() -> None:
    """
    Test case 2: Generate random float with custom range.
    """
    # Act
    result = generate_random_float(5.0, 10.0)

    # Assert
    assert 5.0 <= result <= 10.0


def test_generate_random_float_custom_precision() -> None:
    """
    Test case 3: Generate random float with custom precision.
    """
    # Act
    result = generate_random_float(0.0, 1.0, 4)

    # Assert
    result_str = str(result)
    if "." in result_str:
        decimal_places = len(result_str.split(".")[1])
        assert decimal_places <= 4


def test_generate_random_float_zero_precision() -> None:
    """
    Test case 4: Generate random float with zero precision.
    """
    # Act
    result = generate_random_float(0.0, 10.0, 0)

    # Assert
    assert result == int(result)


def test_generate_random_float_type_error_min_value() -> None:
    """
    Test case 5: TypeError for invalid min_value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="min_value must be a number"):
        generate_random_float("0.0", 1.0)


def test_generate_random_float_type_error_max_value() -> None:
    """
    Test case 6: TypeError for invalid max_value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="max_value must be a number"):
        generate_random_float(0.0, "1.0")


def test_generate_random_float_type_error_precision() -> None:
    """
    Test case 7: TypeError for invalid precision type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="precision must be an integer"):
        generate_random_float(0.0, 1.0, "2")


def test_generate_random_float_value_error_min_greater_than_max() -> None:
    """
    Test case 8: ValueError when min_value > max_value.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="min_value .* must be <= max_value"):
        generate_random_float(10.0, 5.0)


def test_generate_random_float_value_error_negative_precision() -> None:
    """
    Test case 9: ValueError for negative precision.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="precision must be non-negative"):
        generate_random_float(0.0, 1.0, -1)
