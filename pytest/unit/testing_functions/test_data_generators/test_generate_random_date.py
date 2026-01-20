from datetime import date

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from pyutils_collection.testing_functions.test_data_generators.generate_random_date import (
    generate_random_date,
)


def test_generate_random_date_default_parameters() -> None:
    """
    Test case 1: Generate random date with default parameters.
    """
    # Act
    result = generate_random_date()

    # Assert
    assert isinstance(result, date)
    assert 2000 <= result.year <= 2025


def test_generate_random_date_custom_year_range() -> None:
    """
    Test case 2: Generate random date with custom year range.
    """
    # Act
    result = generate_random_date(2020, 2021)

    # Assert
    assert 2020 <= result.year <= 2021


def test_generate_random_date_same_start_end_year() -> None:
    """
    Test case 3: Generate random date when start_year equals end_year.
    """
    # Act
    result = generate_random_date(2022, 2022)

    # Assert
    assert result.year == 2022


def test_generate_random_date_wide_range() -> None:
    """
    Test case 4: Generate random date with wide year range.
    """
    # Act
    result = generate_random_date(1900, 2100)

    # Assert
    assert 1900 <= result.year <= 2100


def test_generate_random_date_type_error_start_year() -> None:
    """
    Test case 5: TypeError for invalid start_year type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="start_year must be an integer"):
        generate_random_date("2000", 2025)


def test_generate_random_date_type_error_end_year() -> None:
    """
    Test case 6: TypeError for invalid end_year type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="end_year must be an integer"):
        generate_random_date(2000, "2025")


def test_generate_random_date_value_error_start_greater_than_end() -> None:
    """
    Test case 7: ValueError when start_year > end_year.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="start_year .* must be <= end_year"):
        generate_random_date(2025, 2020)
