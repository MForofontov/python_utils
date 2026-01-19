import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from python_utils.testing_functions.test_data_generators.generate_random_email import (
    generate_random_email,
)


def test_generate_random_email_default_parameters() -> None:
    """
    Test case 1: Generate random email with default parameters.
    """
    # Act
    result = generate_random_email()

    # Assert
    assert isinstance(result, str)
    assert "@example.com" in result
    assert len(result.split("@")[0]) == 10


def test_generate_random_email_custom_domain() -> None:
    """
    Test case 2: Generate random email with custom domain.
    """
    # Act
    result = generate_random_email("test.org")

    # Assert
    assert "@test.org" in result


def test_generate_random_email_custom_username_length() -> None:
    """
    Test case 3: Generate random email with custom username length.
    """
    # Act
    result = generate_random_email("example.com", 5)

    # Assert
    username = result.split("@")[0]
    assert len(username) == 5


def test_generate_random_email_valid_format() -> None:
    """
    Test case 4: Verify email has valid format.
    """
    # Act
    result = generate_random_email()

    # Assert
    parts = result.split("@")
    assert len(parts) == 2
    assert len(parts[0]) > 0
    assert len(parts[1]) > 0


def test_generate_random_email_type_error_domain() -> None:
    """
    Test case 5: TypeError for invalid domain type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="domain must be a string"):
        generate_random_email(123)


def test_generate_random_email_type_error_username_length() -> None:
    """
    Test case 6: TypeError for invalid username_length type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="username_length must be an integer"):
        generate_random_email("example.com", "10")


def test_generate_random_email_value_error_empty_domain() -> None:
    """
    Test case 7: ValueError for empty domain.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="domain cannot be empty"):
        generate_random_email("")


def test_generate_random_email_value_error_zero_username_length() -> None:
    """
    Test case 8: ValueError for zero username_length.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="username_length must be positive"):
        generate_random_email("example.com", 0)


def test_generate_random_email_value_error_negative_username_length() -> None:
    """
    Test case 9: ValueError for negative username_length.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="username_length must be positive"):
        generate_random_email("example.com", -5)
