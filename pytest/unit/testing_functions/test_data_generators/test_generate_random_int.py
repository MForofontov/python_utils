import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from testing_functions.test_data_generators.generate_random_int import (
    generate_random_int,
)


def test_generate_random_int_default_parameters() -> None:
    """
    Test case 1: Generate random int with default parameters.
    """
    # Act
    result = generate_random_int()

    # Assert
    assert isinstance(result, int)
    assert 0 <= result <= 100


def test_generate_random_int_custom_range() -> None:
    """
    Test case 2: Generate random int with custom range.
    """
    # Act
    result = generate_random_int(10, 20)

    # Assert
    assert 10 <= result <= 20


def test_generate_random_int_same_min_max() -> None:
    """
    Test case 3: Generate random int when min equals max.
    """
    # Act
    result = generate_random_int(5, 5)

    # Assert
    assert result == 5


def test_generate_random_int_negative_range() -> None:
    """
    Test case 4: Generate random int with negative range.
    """
    # Act
    result = generate_random_int(-10, -5)

    # Assert
    assert -10 <= result <= -5


def test_generate_random_int_type_error_min_value() -> None:
    """
    Test case 5: TypeError for invalid min_value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="min_value must be an integer"):
        generate_random_int("0", 10)


def test_generate_random_int_type_error_max_value() -> None:
    """
    Test case 6: TypeError for invalid max_value type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="max_value must be an integer"):
        generate_random_int(0, "10")


def test_generate_random_int_value_error_min_greater_than_max() -> None:
    """
    Test case 7: ValueError when min_value > max_value.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="min_value .* must be <= max_value"):
        generate_random_int(10, 5)
