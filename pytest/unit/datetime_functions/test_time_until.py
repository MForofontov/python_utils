import pytest
from datetime import datetime, date
from datetime_functions.time_until import time_until


def test_time_until_seconds() -> None:
    """
    Test case 1: Test time_until function with seconds difference.
    """
    past_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future_dt: datetime = datetime(2023, 1, 15, 12, 0, 30)
    result: str = time_until(future_dt, past_dt)
    assert isinstance(result, str)
    assert "30 seconds" in result or "in a moment" in result


def test_time_until_minutes() -> None:
    """
    Test case 2: Test time_until function with minutes difference.
    """
    past_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future_dt: datetime = datetime(2023, 1, 15, 12, 15, 0)
    result: str = time_until(future_dt, past_dt)
    assert isinstance(result, str)
    assert "15 minutes" in result


def test_time_until_hours() -> None:
    """
    Test case 3: Test time_until function with hours difference.
    """
    past_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future_dt: datetime = datetime(2023, 1, 15, 15, 0, 0)
    result: str = time_until(future_dt, past_dt)
    assert isinstance(result, str)
    assert "3 hours" in result


def test_time_until_days() -> None:
    """
    Test case 4: Test time_until function with days difference.
    """
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2023, 1, 20)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "5 days" in result


def test_time_until_weeks() -> None:
    """
    Test case 5: Test time_until function with weeks difference.
    """
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2023, 2, 5)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "week" in result


def test_time_until_months() -> None:
    """
    Test case 6: Test time_until function with months difference.
    """
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2023, 6, 15)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "month" in result


def test_time_until_years() -> None:
    """
    Test case 7: Test time_until function with years difference.
    """
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2025, 1, 15)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "year" in result


def test_time_until_mixed_types() -> None:
    """
    Test case 8: Test time_until function with mixed date and datetime objects.
    """
    past_date: date = date(2023, 1, 15)
    future_dt: datetime = datetime(2023, 1, 20, 12, 0, 0)
    result: str = time_until(future_dt, past_date)
    assert isinstance(result, str)
    assert "day" in result


def test_time_until_invalid_input_type() -> None:
    """
    Test case 9: Test time_until function with invalid input type raises TypeError.
    """
    test_date: date = date(2023, 1, 20)
    
    with pytest.raises(TypeError):
        time_until('2023-01-15', test_date)
    
    with pytest.raises(TypeError):
        time_until(123, test_date)
    
    with pytest.raises(TypeError):
        time_until(None, test_date)


def test_time_until_past_date_error() -> None:
    """
    Test case 10: Test time_until function with past date raises ValueError.
    """
    future_date: date = date(2023, 1, 15)
    past_date: date = date(2023, 1, 20)
    
    with pytest.raises(ValueError):
        time_until(future_date, past_date)
