import pytest
from datetime import datetime, date
from datetime_functions.get_start_of_month import get_start_of_month


def test_get_start_of_month_january() -> None:
    """
    Test get_start_of_month function with January.
    """
    # Test case 1: January (mid-month)
    test_date: date = date(2023, 1, 15)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 1)


def test_get_start_of_month_february() -> None:
    """
    Test get_start_of_month function with February.
    """
    # Test case 2: February (end of month)
    test_date: date = date(2023, 2, 28)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 2, 1)


def test_get_start_of_month_february_leap() -> None:
    """
    Test get_start_of_month function with February in leap year.
    """
    # Test case 3: February leap year
    test_date: date = date(2020, 2, 29)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2020, 2, 1)


def test_get_start_of_month_december() -> None:
    """
    Test get_start_of_month function with December.
    """
    # Test case 4: December (New Year's Eve)
    test_date: date = date(2023, 12, 31)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 12, 1)


def test_get_start_of_month_with_datetime() -> None:
    """
    Test get_start_of_month function with datetime object.
    """
    # Test case 5: Datetime object
    test_datetime: datetime = datetime(2023, 6, 15, 14, 30, 45)
    result: date = get_start_of_month(test_datetime)
    assert isinstance(result, date)
    assert result == date(2023, 6, 1)


def test_get_start_of_month_already_first_day() -> None:
    """
    Test get_start_of_month function when input is already the first day.
    """
    # Test case 6: Already first day of month
    test_date: date = date(2023, 3, 1)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 3, 1)


def test_get_start_of_month_last_day() -> None:
    """
    Test get_start_of_month function when input is the last day.
    """
    # Test case 7: Last day of month
    test_date: date = date(2023, 5, 31)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 5, 1)


def test_get_start_of_month_april() -> None:
    """
    Test get_start_of_month function with April.
    """
    # Test case 8: April (30 days)
    test_date: date = date(2023, 4, 15)
    result: date = get_start_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 4, 1)


def test_get_start_of_month_invalid_input_type() -> None:
    """
    Test get_start_of_month function with invalid input type raises TypeError.
    """
    # Test case 9: Invalid input types
    with pytest.raises(TypeError):
        get_start_of_month('2023-01-15')
    
    with pytest.raises(TypeError):
        get_start_of_month(123)
    
    with pytest.raises(TypeError):
        get_start_of_month(None)
