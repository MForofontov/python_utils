import pytest
from datetime import datetime, date
from datetime_functions.time_until import time_until


def test_time_until_seconds() -> None:
    """
    Test time_until function with seconds difference.
    """
    # Test case 1: Seconds difference
    past_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future_dt: datetime = datetime(2023, 1, 15, 12, 0, 30)
    result: str = time_until(future_dt, past_dt)
    assert isinstance(result, str)
    assert "30 seconds" in result or "in a moment" in result


def test_time_until_minutes() -> None:
    """
    Test time_until function with minutes difference.
    """
    # Test case 2: Minutes difference
    past_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future_dt: datetime = datetime(2023, 1, 15, 12, 15, 0)
    result: str = time_until(future_dt, past_dt)
    assert isinstance(result, str)
    assert "15 minutes" in result


def test_time_until_hours() -> None:
    """
    Test time_until function with hours difference.
    """
    # Test case 3: Hours difference
    past_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future_dt: datetime = datetime(2023, 1, 15, 15, 0, 0)
    result: str = time_until(future_dt, past_dt)
    assert isinstance(result, str)
    assert "3 hours" in result


def test_time_until_days() -> None:
    """
    Test time_until function with days difference.
    """
    # Test case 4: Days difference
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2023, 1, 20)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "5 days" in result


def test_time_until_weeks() -> None:
    """
    Test time_until function with weeks difference.
    """
    # Test case 5: Weeks difference
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2023, 2, 5)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "week" in result


def test_time_until_months() -> None:
    """
    Test time_until function with months difference.
    """
    # Test case 6: Months difference
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2023, 6, 15)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "month" in result


def test_time_until_years() -> None:
    """
    Test time_until function with years difference.
    """
    # Test case 7: Years difference
    past_date: date = date(2023, 1, 15)
    future_date: date = date(2025, 1, 15)
    result: str = time_until(future_date, past_date)
    assert isinstance(result, str)
    assert "year" in result


def test_time_until_mixed_types() -> None:
    """
    Test time_until function with mixed date and datetime objects.
    """
    # Test case 8: Mixed types
    past_date: date = date(2023, 1, 15)
    future_dt: datetime = datetime(2023, 1, 20, 12, 0, 0)
    result: str = time_until(future_dt, past_date)
    assert isinstance(result, str)
    assert "day" in result


def test_time_until_invalid_input_type() -> None:
    """
    Test time_until function with invalid input type raises TypeError.
    """
    # Test case 9: Invalid input types
    test_date: date = date(2023, 1, 20)
    
    with pytest.raises(TypeError):
        time_until('2023-01-15', test_date)
    
    with pytest.raises(TypeError):
        time_until(123, test_date)
    
    with pytest.raises(TypeError):
        time_until(None, test_date)


def test_time_until_past_date_error() -> None:
    """
    Test time_until function with past date raises ValueError.
    """
    # Test case 10: Past date error
    future_date: date = date(2023, 1, 15)
    past_date: date = date(2023, 1, 20)
    
    with pytest.raises(ValueError):
        time_until(future_date, past_date)
