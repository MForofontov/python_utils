import pytest
from datetime import datetime, date
from datetime_functions.time_ago import time_ago


def test_time_ago_seconds() -> None:
    """
    Test case 1: Test time_ago function with seconds difference.
    """
    reference: datetime = datetime(2023, 1, 15, 12, 0, 30)
    past: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: str = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "30 seconds ago"


def test_time_ago_minutes() -> None:
    """
    Test case 2: Test time_ago function with minutes difference.
    """
    reference: datetime = datetime(2023, 1, 15, 12, 30, 0)
    past: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: str = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "30 minutes ago"


def test_time_ago_hours() -> None:
    """
    Test case 3: Test time_ago function with hours difference.
    """
    reference: datetime = datetime(2023, 1, 15, 15, 0, 0)
    past: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: str = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "3 hours ago"


def test_time_ago_days() -> None:
    """
    Test case 4: Test time_ago function with days difference.
    """
    reference: date = date(2023, 1, 18)
    past: date = date(2023, 1, 15)
    result: str = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "3 days ago"


def test_time_ago_weeks() -> None:
    """
    Test case 5: Test time_ago function with weeks difference.
    """
    reference: date = date(2023, 2, 5)
    past: date = date(2023, 1, 15)
    result: str = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "3 weeks ago"


def test_time_ago_just_now() -> None:
    """
    Test case 6: Test time_ago function with very recent time.
    """
    reference: datetime = datetime(2023, 1, 15, 12, 0, 5)
    past: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: str = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "just now"


def test_time_ago_future_date_error() -> None:
    """
    Test case 7: Test time_ago function with future date raises ValueError.
    """
    reference: datetime = datetime(2023, 1, 15, 12, 0, 0)
    future: datetime = datetime(2023, 1, 15, 13, 0, 0)

    with pytest.raises(ValueError):
        time_ago(future, reference)


def test_time_ago_invalid_input_type() -> None:
    """
    Test case 8: Test time_ago function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        time_ago("2023-01-15")

    with pytest.raises(TypeError):
        time_ago(123)

    with pytest.raises(TypeError):
        time_ago(None)
