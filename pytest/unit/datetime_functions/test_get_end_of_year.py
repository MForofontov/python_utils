"""Unit tests for get_end_of_year function."""
from datetime import datetime

import pytest

from datetime_functions.get_end_of_year import get_end_of_year


def test_get_end_of_year_mid_year() -> None:
    """
    Test case 1: Get end of year for mid-year date.
    """
    # Arrange
    date_obj = datetime(2023, 6, 15, 10, 30, 45)

    # Act
    result = get_end_of_year(date_obj)

    # Assert
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31
    assert result.hour == 10
    assert result.minute == 30
    assert result.second == 45


def test_get_end_of_year_beginning_of_year() -> None:
    """
    Test case 2: Get end of year for beginning of year.
    """
    # Arrange
    date_obj = datetime(2023, 1, 1, 0, 0, 0)

    # Act
    result = get_end_of_year(date_obj)

    # Assert
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31
    assert result.hour == 0
    assert result.minute == 0
    assert result.second == 0


def test_get_end_of_year_already_end_of_year() -> None:
    """
    Test case 3: Get end of year when already at end of year.
    """
    # Arrange
    date_obj = datetime(2023, 12, 31, 23, 59, 59)

    # Act
    result = get_end_of_year(date_obj)

    # Assert
    assert result.year == 2023
    assert result.month == 12
    assert result.day == 31
    assert result.hour == 23
    assert result.minute == 59
    assert result.second == 59


def test_get_end_of_year_leap_year() -> None:
    """
    Test case 4: Get end of year for leap year.
    """
    # Arrange
    date_obj = datetime(2024, 2, 29, 12, 0, 0)

    # Act
    result = get_end_of_year(date_obj)

    # Assert
    assert result.year == 2024
    assert result.month == 12
    assert result.day == 31


def test_get_end_of_year_preserves_time() -> None:
    """
    Test case 5: Verify time components are preserved.
    """
    # Arrange
    date_obj = datetime(2023, 3, 15, 14, 25, 36)

    # Act
    result = get_end_of_year(date_obj)

    # Assert
    assert result.hour == 14
    assert result.minute == 25
    assert result.second == 36


def test_get_end_of_year_type_error_non_datetime() -> None:
    """
    Test case 6: TypeError when input is not a datetime object.
    """
    # Arrange
    invalid_input = "2023-12-31"

    # Act & Assert
    with pytest.raises(TypeError, match="date_obj must be a datetime object"):
        get_end_of_year(invalid_input)  # type: ignore


def test_get_end_of_year_type_error_none() -> None:
    """
    Test case 7: TypeError when input is None.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="date_obj must be a datetime object"):
        get_end_of_year(None)  # type: ignore


def test_get_end_of_year_different_years() -> None:
    """
    Test case 8: Get end of year for different years.
    """
    # Arrange
    dates = [
        datetime(2020, 5, 10, 0, 0, 0),
        datetime(2021, 8, 15, 12, 0, 0),
        datetime(2022, 11, 20, 23, 59, 59),
    ]

    # Act & Assert
    for date in dates:
        result = get_end_of_year(date)
        assert result.year == date.year
        assert result.month == 12
        assert result.day == 31
