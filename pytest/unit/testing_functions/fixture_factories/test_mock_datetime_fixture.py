from datetime import datetime

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.testing]
from testing_functions.fixture_factories.mock_datetime_fixture import (
    mock_datetime_fixture,
)


def test_mock_datetime_fixture_default_parameters() -> None:
    """
    Test case 1: Mock datetime with default parameters.
    """
    # Act & Assert
    with mock_datetime_fixture() as mock_dt:
        assert isinstance(mock_dt, datetime)
        assert mock_dt.year == 2025
        assert mock_dt.month == 1
        assert mock_dt.day == 1


def test_mock_datetime_fixture_custom_date() -> None:
    """
    Test case 2: Mock datetime with custom date.
    """
    # Act & Assert
    with mock_datetime_fixture(2024, 12, 25) as mock_dt:
        assert mock_dt.year == 2024
        assert mock_dt.month == 12
        assert mock_dt.day == 25


def test_mock_datetime_fixture_custom_time() -> None:
    """
    Test case 3: Mock datetime with custom time.
    """
    # Act & Assert
    with mock_datetime_fixture(2025, 1, 1, 14, 30, 45) as mock_dt:
        assert mock_dt.hour == 14
        assert mock_dt.minute == 30
        assert mock_dt.second == 45


def test_mock_datetime_fixture_midnight() -> None:
    """
    Test case 4: Mock datetime at midnight.
    """
    # Act & Assert
    with mock_datetime_fixture(2025, 1, 1, 0, 0, 0) as mock_dt:
        assert mock_dt.hour == 0
        assert mock_dt.minute == 0
        assert mock_dt.second == 0


def test_mock_datetime_fixture_end_of_day() -> None:
    """
    Test case 5: Mock datetime at end of day.
    """
    # Act & Assert
    with mock_datetime_fixture(2025, 12, 31, 23, 59, 59) as mock_dt:
        assert mock_dt.month == 12
        assert mock_dt.day == 31
        assert mock_dt.hour == 23
        assert mock_dt.minute == 59
        assert mock_dt.second == 59


def test_mock_datetime_fixture_type_error_year() -> None:
    """
    Test case 6: TypeError for invalid year type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="year must be an integer"):
        with mock_datetime_fixture("2025"):
            pass


def test_mock_datetime_fixture_type_error_month() -> None:
    """
    Test case 7: TypeError for invalid month type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="month must be an integer"):
        with mock_datetime_fixture(2025, "1"):
            pass


def test_mock_datetime_fixture_type_error_day() -> None:
    """
    Test case 8: TypeError for invalid day type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="day must be an integer"):
        with mock_datetime_fixture(2025, 1, "1"):
            pass


def test_mock_datetime_fixture_type_error_hour() -> None:
    """
    Test case 9: TypeError for invalid hour type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="hour must be an integer"):
        with mock_datetime_fixture(2025, 1, 1, "14"):
            pass


def test_mock_datetime_fixture_type_error_minute() -> None:
    """
    Test case 10: TypeError for invalid minute type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="minute must be an integer"):
        with mock_datetime_fixture(2025, 1, 1, 14, "30"):
            pass


def test_mock_datetime_fixture_type_error_second() -> None:
    """
    Test case 11: TypeError for invalid second type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="second must be an integer"):
        with mock_datetime_fixture(2025, 1, 1, 14, 30, "45"):
            pass
