import pytest
from datetime import datetime, date
from datetime_functions.get_end_of_week import get_end_of_week


def test_get_end_of_week_monday() -> None:
    """
    Test get_end_of_week function starting from Monday.
    """
    # Test case 1: Monday (week should end on Sunday)
    test_date: date = date(2023, 6, 5)  # Monday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_tuesday() -> None:
    """
    Test get_end_of_week function starting from Tuesday.
    """
    # Test case 2: Tuesday
    test_date: date = date(2023, 6, 6)  # Tuesday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_saturday() -> None:
    """
    Test get_end_of_week function starting from Saturday.
    """
    # Test case 3: Saturday
    test_date: date = date(2023, 6, 10)  # Saturday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_sunday() -> None:
    """
    Test get_end_of_week function starting from Sunday.
    """
    # Test case 4: Sunday (already end of week)
    test_date: date = date(2023, 6, 11)  # Sunday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Same Sunday


def test_get_end_of_week_with_datetime() -> None:
    """
    Test get_end_of_week function with datetime object.
    """
    # Test case 5: Datetime object (Wednesday)
    test_datetime: datetime = datetime(2023, 6, 7, 14, 30, 45)  # Wednesday
    result: date = get_end_of_week(test_datetime)
    assert isinstance(result, date)
    assert result == date(2023, 6, 11)  # Sunday


def test_get_end_of_week_cross_month_boundary() -> None:
    """
    Test get_end_of_week function crossing month boundary.
    """
    # Test case 6: Week crosses month boundary
    test_date: date = date(2023, 5, 29)  # Monday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 6, 4)  # Sunday in next month


def test_get_end_of_week_cross_year_boundary() -> None:
    """
    Test get_end_of_week function crossing year boundary.
    """
    # Test case 7: Week crosses year boundary
    test_date: date = date(2022, 12, 26)  # Monday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 1)  # Sunday in next year


def test_get_end_of_week_friday_the_13th() -> None:
    """
    Test get_end_of_week function with Friday the 13th.
    """
    # Test case 8: Friday the 13th
    test_date: date = date(2023, 1, 13)  # Friday
    result: date = get_end_of_week(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 15)  # Sunday


def test_get_end_of_week_invalid_input_type() -> None:
    """
    Test get_end_of_week function with invalid input type raises TypeError.
    """
    # Test case 9: Invalid input types
    with pytest.raises(TypeError):
        get_end_of_week('2023-06-05')
    
    with pytest.raises(TypeError):
        get_end_of_week(123)
    
    with pytest.raises(TypeError):
        get_end_of_week(None)
