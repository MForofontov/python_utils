from datetime import datetime

import pytest

try:
    import pytz
    from python_utils.datetime_functions.get_end_of_week import get_end_of_week
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    get_end_of_week = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.datetime,
    pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed"),
]


def test_get_end_of_week_default() -> None:
    """
    Test case 1: get_end_of_week returns correct end of week for default start (Sunday).
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    result = get_end_of_week(dt)
    assert result == datetime(2023, 6, 11, 14, 30, 45)


def test_get_end_of_week_custom_start() -> None:
    """
    Test case 2: get_end_of_week returns correct end of week for custom start (Saturday).
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    result = get_end_of_week(dt, start_of_week=6)
    assert result == datetime(2023, 6, 10, 14, 30, 45)


def test_get_end_of_week_month_boundary() -> None:
    """
    Test case 3: get_end_of_week handles month boundary correctly.
    """
    dt = datetime(2023, 4, 28, 9, 0)
    result = get_end_of_week(dt)
    assert result == datetime(2023, 4, 30, 9, 0)


def test_get_end_of_week_year_boundary() -> None:
    """
    Test case 4: get_end_of_week handles year boundary correctly.
    """
    dt = datetime(2022, 12, 30, 23, 59)
    result = get_end_of_week(dt)
    assert result == datetime(2023, 1, 1, 23, 59)


def test_get_end_of_week_week_wraps_around() -> None:
    """
    Test case 5: Test get_end_of_week when current day is after end of week (else branch).
    """
    # Friday (day 4) with start_of_week=0 (Monday), end should be Sunday (day 6)
    # This tests the else branch where current_weekday > end_of_week_day
    dt = datetime(2023, 6, 9, 12, 0, 0)  # Friday
    result = get_end_of_week(dt, start_of_week=0)  # End should be Sunday
    # Friday is day 4, end of week (Sunday) is day 6, which is 2 days ahead
    expected = datetime(2023, 6, 11)  # Sunday
    assert result.date() == expected.date()


def test_get_end_of_week_type_error() -> None:
    """
    Test case 6: get_end_of_week raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_end_of_week("2023-06-07")
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_end_of_week(123)


def test_get_end_of_week_value_error() -> None:
    """
    Test case 7: get_end_of_week raises ValueError for invalid start_of_week argument.
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    with pytest.raises(
        ValueError, match="start_of_week must be an integer between 0 and 6"
    ):
        get_end_of_week(dt, start_of_week=7)
