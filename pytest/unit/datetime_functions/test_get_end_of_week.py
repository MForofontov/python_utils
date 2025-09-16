from datetime import date, datetime

import pytest
from datetime_functions.get_end_of_week import get_end_of_week


def test_get_end_of_week_monday() -> None:
    """
    Test case 1: Test get_end_of_week function starting from Monday.
    """
    test_date: date = date(2023, 6, 5)  # Monday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_tuesday() -> None:
    """
    Test case 2: Test get_end_of_week function starting from Tuesday.
    """
    test_date: date = date(2023, 6, 6)  # Tuesday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_saturday() -> None:
    """
    Test case 3: Test get_end_of_week function starting from Saturday.
    """
    test_date: date = date(2023, 6, 10)  # Saturday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_sunday() -> None:
    """
    Test case 4: Test get_end_of_week function starting from Sunday.
    """
    test_date: date = date(2023, 6, 11)  # Sunday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Same Sunday


def test_get_end_of_week_with_datetime() -> None:
    """
    Test case 5: Test get_end_of_week function with datetime object.
    """
    test_datetime: datetime = datetime(2023, 6, 7, 14, 30, 45)  # Wednesday
    result: date = get_end_of_week(test_datetime)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_cross_month_boundary() -> None:
    """
    Test case 6: Test get_end_of_week function crossing month boundary.
    """
    test_date: date = date(2023, 5, 29)  # Monday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 4)  # Sunday in next month


def test_get_end_of_week_cross_year_boundary() -> None:
    """
    Test case 7: Test get_end_of_week function crossing year boundary.
    """
    test_date: date = date(2022, 12, 26)  # Monday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 1)  # Sunday in next year


def test_get_end_of_week_friday_the_13th() -> None:
    """
    Test case 8: Test get_end_of_week function with Friday the 13th.
    """
    test_date: date = date(2023, 1, 13)  # Friday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 15)  # Sunday


def test_get_end_of_week_invalid_input_type() -> None:
    """
    Test case 9: Test get_end_of_week function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_end_of_week("2023-06-05")

    with pytest.raises(TypeError):
        get_end_of_week(123)

    with pytest.raises(TypeError):
        get_end_of_week(None)
