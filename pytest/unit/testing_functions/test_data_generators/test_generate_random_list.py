import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from testing_functions.test_data_generators.generate_random_list import (
    generate_random_list,
)


def test_generate_random_list_default_parameters() -> None:
    """
    Test case 1: Generate random list with default parameters.
    """
    # Act
    result = generate_random_list()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 10
    assert all(isinstance(x, int) for x in result)


def test_generate_random_list_custom_length() -> None:
    """
    Test case 2: Generate random list with custom length.
    """
    # Act
    result = generate_random_list(5)

    # Assert
    assert len(result) == 5


def test_generate_random_list_float_type() -> None:
    """
    Test case 3: Generate random list of floats.
    """
    # Act
    result = generate_random_list(10, "float")

    # Assert
    assert all(isinstance(x, float) for x in result)


def test_generate_random_list_string_type() -> None:
    """
    Test case 4: Generate random list of strings.
    """
    # Act
    result = generate_random_list(10, "str")

    # Assert
    assert all(isinstance(x, str) for x in result)


def test_generate_random_list_custom_range() -> None:
    """
    Test case 5: Generate random list with custom value range.
    """
    # Act
    result = generate_random_list(10, "int", 1, 10)

    # Assert
    assert all(1 <= x <= 10 for x in result)


def test_generate_random_list_empty_list() -> None:
    """
    Test case 6: Generate empty list.
    """
    # Act
    result = generate_random_list(0)

    # Assert
    assert result == []


def test_generate_random_list_type_error_length() -> None:
    """
    Test case 7: TypeError for invalid length type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="length must be an integer"):
        generate_random_list("10")


def test_generate_random_list_type_error_element_type() -> None:
    """
    Test case 8: TypeError for invalid element_type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="element_type must be a string"):
        generate_random_list(10, 123)


def test_generate_random_list_value_error_negative_length() -> None:
    """
    Test case 9: ValueError for negative length.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="length must be non-negative"):
        generate_random_list(-1)


def test_generate_random_list_value_error_invalid_element_type() -> None:
    """
    Test case 10: ValueError for invalid element_type value.
    """
    # Act & Assert
    with pytest.raises(
        ValueError, match="element_type must be 'int', 'float', or 'str'"
    ):
        generate_random_list(10, "boolean")
