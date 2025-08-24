import pytest
from datetime import datetime, date
from datetime_functions.get_end_of_month import get_end_of_month


def test_get_end_of_month_january() -> None:
    """
    Test case 1: Test get_end_of_month function with January.
    """
    test_date: date = date(2023, 1, 15)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 1, 31)


def test_get_end_of_month_february_non_leap() -> None:
    """
    Test case 2: Test get_end_of_month function with February in non-leap year.
    """
    test_date: date = date(2023, 2, 10)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 2, 28)


def test_get_end_of_month_february_leap() -> None:
    """
    Test case 3: Test get_end_of_month function with February in leap year.
    """
    test_date: date = date(2020, 2, 15)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2020, 2, 29)


def test_get_end_of_month_april() -> None:
    """
    Test case 4: Test get_end_of_month function with April.
    """
    test_date: date = date(2023, 4, 5)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 4, 30)


def test_get_end_of_month_december() -> None:
    """
    Test case 5: Test get_end_of_month function with December.
    """
    test_date: date = date(2023, 12, 1)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 12, 31)


def test_get_end_of_month_with_datetime() -> None:
    """
    Test case 6: Test get_end_of_month function with datetime object.
    """
    test_datetime: datetime = datetime(2023, 6, 15, 12, 30, 45)
    result: date = get_end_of_month(test_datetime)
    assert isinstance(result, date)
    assert result == date(2023, 6, 30)


def test_get_end_of_month_already_last_day() -> None:
    """
    Test case 7: Test get_end_of_month function when input is already the last day.
    """
    test_date: date = date(2023, 3, 31)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 3, 31)


def test_get_end_of_month_first_day() -> None:
    """
    Test case 8: Test get_end_of_month function when input is the first day.
    """
    test_date: date = date(2023, 5, 1)
    result: date = get_end_of_month(test_date)
    assert isinstance(result, date)
    assert result == date(2023, 5, 31)


def test_get_end_of_month_invalid_input_type() -> None:
    """
    Test case 9: Test get_end_of_month function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_end_of_month('2023-01-15')
    
    with pytest.raises(TypeError):
        get_end_of_month(123)
    
    with pytest.raises(TypeError):
        get_end_of_month(None)
