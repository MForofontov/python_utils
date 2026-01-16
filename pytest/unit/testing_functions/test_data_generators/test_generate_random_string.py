import string

import pytest
from testing_functions.test_data_generators.generate_random_string import (
    generate_random_string,
)


def test_generate_random_string_default_parameters() -> None:
    """
    Test case 1: Generate random string with default parameters.
    """
    # Act
    result = generate_random_string()

    # Assert
    assert isinstance(result, str)
    assert len(result) == 10
    assert all(c in string.ascii_letters + string.digits for c in result)


def test_generate_random_string_custom_length() -> None:
    """
    Test case 2: Generate random string with custom length.
    """
    # Arrange
    length = 20

    # Act
    result = generate_random_string(length)

    # Assert
    assert len(result) == 20


def test_generate_random_string_custom_charset() -> None:
    """
    Test case 3: Generate random string with custom character set.
    """
    # Arrange
    charset = "ABC123"

    # Act
    result = generate_random_string(10, charset)

    # Assert
    assert all(c in charset for c in result)


def test_generate_random_string_single_character() -> None:
    """
    Test case 4: Generate random string with length 1.
    """
    # Act
    result = generate_random_string(1)

    # Assert
    assert len(result) == 1


def test_generate_random_string_type_error_length() -> None:
    """
    Test case 5: TypeError for invalid length type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="length must be an integer"):
        generate_random_string("10")


def test_generate_random_string_type_error_charset() -> None:
    """
    Test case 6: TypeError for invalid charset type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="charset must be a string"):
        generate_random_string(10, 123)


def test_generate_random_string_value_error_negative_length() -> None:
    """
    Test case 7: ValueError for negative length.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="length must be positive"):
        generate_random_string(-1)


def test_generate_random_string_value_error_zero_length() -> None:
    """
    Test case 8: ValueError for zero length.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="length must be positive"):
        generate_random_string(0)


def test_generate_random_string_value_error_empty_charset() -> None:
    """
    Test case 9: ValueError for empty charset.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="charset cannot be empty"):
        generate_random_string(10, "")
