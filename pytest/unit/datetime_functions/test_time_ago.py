from datetime import datetime

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.datetime]
from python_utils.datetime_functions.time_ago import time_ago


def test_time_ago_seconds() -> None:
    """
    Test case 1: time_ago returns correct string for seconds difference.
    """
    reference = datetime(2023, 1, 15, 12, 0, 30)
    past = datetime(2023, 1, 15, 12, 0, 0)
    result = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "30 seconds ago"


def test_time_ago_minutes() -> None:
    """
    Test case 2: time_ago returns correct string for minutes difference.
    """
    reference = datetime(2023, 1, 15, 12, 30, 0)
    past = datetime(2023, 1, 15, 12, 0, 0)
    result = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "30 minutes ago"


def test_time_ago_hours() -> None:
    """
    Test case 3: time_ago returns correct string for hours difference.
    """
    reference = datetime(2023, 1, 15, 15, 0, 0)
    past = datetime(2023, 1, 15, 12, 0, 0)
    result = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "3 hours ago"


def test_time_ago_days() -> None:
    """
    Test case 4: time_ago returns correct string for days difference.
    """
    reference = datetime(2023, 1, 18, 0, 0, 0)
    past = datetime(2023, 1, 15, 0, 0, 0)
    result = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "3 days ago"


def test_time_ago_weeks() -> None:
    """
    Test case 5: time_ago returns correct string for weeks difference.
    """
    reference = datetime(2023, 2, 5, 0, 0, 0)
    past = datetime(2023, 1, 15, 0, 0, 0)
    result = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "3 weeks ago"


def test_time_ago_just_now() -> None:
    """
    Test case 6: time_ago returns 'just now' for very recent times.
    """
    reference = datetime(2023, 1, 15, 12, 0, 5)
    past = datetime(2023, 1, 15, 12, 0, 0)
    result = time_ago(past, reference)
    assert isinstance(result, str)
    assert result == "just now"


def test_time_ago_future_value_error() -> None:
    """
    Test case 7: time_ago raises ValueError if the first argument is in the future relative to reference.
    """
    reference = datetime(2023, 1, 15, 12, 0, 0)
    future = datetime(2023, 1, 15, 13, 0, 0)
    with pytest.raises(ValueError):
        time_ago(future, reference)


def test_time_ago_invalid_type() -> None:
    """
    Test case 8: time_ago raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError):
        time_ago("2023-01-15")
    with pytest.raises(TypeError):
        time_ago(123)
    with pytest.raises(TypeError):
        time_ago(None)
