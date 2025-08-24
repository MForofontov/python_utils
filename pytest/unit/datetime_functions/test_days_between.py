import pytest
from datetime import datetime, date
from datetime_functions.days_between import days_between


def test_days_between_positive_difference() -> None:
    """
    Test case 1: Test days_between function with positive difference.
    """
    date1: date = date(2023, 1, 15)
    date2: date = date(2023, 1, 20)
    result: int = days_between(date1, date2)
    assert isinstance(result, int)
    assert result == 5


def test_days_between_negative_difference() -> None:
    """
    Test case 2: Test days_between function with negative difference.
    """
    date1: date = date(2023, 1, 20)
    date2: date = date(2023, 1, 15)
    result: int = days_between(date1, date2)
    assert isinstance(result, int)
    assert result == -5


def test_days_between_same_dates() -> None:
    """
    Test case 3: Test days_between function with same dates.
    """
    date1: date = date(2023, 1, 15)
    date2: date = date(2023, 1, 15)
    result: int = days_between(date1, date2)
    assert isinstance(result, int)
    assert result == 0


def test_days_between_with_datetime_objects() -> None:
    """
    Test case 4: Test days_between function with datetime objects.
    """
    dt1: datetime = datetime(2023, 1, 15, 10, 30, 0)
    dt2: datetime = datetime(2023, 1, 18, 20, 45, 0)
    result: int = days_between(dt1, dt2)
    assert isinstance(result, int)
    assert result == 3


def test_days_between_mixed_types() -> None:
    """
    Test case 5: Test days_between function with mixed date and datetime objects.
    """
    date1: date = date(2023, 1, 15)
    dt2: datetime = datetime(2023, 1, 20, 12, 0, 0)
    result: int = days_between(date1, dt2)
    assert isinstance(result, int)
    assert result == 5


def test_days_between_cross_month() -> None:
    """
    Test case 6: Test days_between function across month boundaries.
    """
    date1: date = date(2023, 1, 30)
    date2: date = date(2023, 2, 2)
    result: int = days_between(date1, date2)
    assert isinstance(result, int)
    assert result == 3


def test_days_between_invalid_input_type() -> None:
    """
    Test case 7: Test days_between function with invalid input type raises TypeError.
    """
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(TypeError):
        days_between('2023-01-15', test_date)
    
    with pytest.raises(TypeError):
        days_between(test_date, '2023-01-20')
    
    with pytest.raises(TypeError):
        days_between(123, test_date)
    
    with pytest.raises(TypeError):
        days_between(test_date, None)
