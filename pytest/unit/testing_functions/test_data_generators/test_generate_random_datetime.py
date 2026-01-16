from datetime import datetime

import pytest
from testing_functions.test_data_generators.generate_random_datetime import (
    generate_random_datetime,
)


def test_generate_random_datetime_default_parameters() -> None:
    """
    Test case 1: Generate random datetime with default parameters.
    """
    # Act
    result = generate_random_datetime()

    # Assert
    assert isinstance(result, datetime)
    assert 2000 <= result.year <= 2025
    assert 0 <= result.hour <= 23
    assert 0 <= result.minute <= 59
    assert 0 <= result.second <= 59


def test_generate_random_datetime_custom_year_range() -> None:
    """
    Test case 2: Generate random datetime with custom year range.
    """
    # Act
    result = generate_random_datetime(2020, 2021)

    # Assert
    assert 2020 <= result.year <= 2021


def test_generate_random_datetime_same_start_end_year() -> None:
    """
    Test case 3: Generate random datetime when start_year equals end_year.
    """
    # Act
    result = generate_random_datetime(2022, 2022)

    # Assert
    assert result.year == 2022


def test_generate_random_datetime_has_time_component() -> None:
    """
    Test case 4: Verify datetime has time component (not just date).
    """
    # Act
    results = [generate_random_datetime() for _ in range(10)]

    # Assert - at least one should have non-zero time
    has_time = any(r.hour != 0 or r.minute != 0 or r.second != 0 for r in results)
    assert has_time


def test_generate_random_datetime_type_error_start_year() -> None:
    """
    Test case 5: TypeError for invalid start_year type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="start_year must be an integer"):
        generate_random_datetime("2000", 2025)


def test_generate_random_datetime_type_error_end_year() -> None:
    """
    Test case 6: TypeError for invalid end_year type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="end_year must be an integer"):
        generate_random_datetime(2000, "2025")


def test_generate_random_datetime_value_error_start_greater_than_end() -> None:
    """
    Test case 7: ValueError when start_year > end_year.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="start_year .* must be <= end_year"):
        generate_random_datetime(2025, 2020)
