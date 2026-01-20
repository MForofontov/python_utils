from datetime import datetime

import pytest

try:
    import pytz
    from pyutils_collection.datetime_functions.get_start_of_week import get_start_of_week
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    get_start_of_week = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.datetime,
    pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed"),
]


def test_get_start_of_week_default() -> None:
    """
    Test case 1: get_start_of_week returns correct start of week for default start (Monday).
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    result = get_start_of_week(dt)
    assert result == datetime(2023, 6, 5, 14, 30, 45)


def test_get_start_of_week_custom_start() -> None:
    """
    Test case 2: get_start_of_week returns correct start of week for custom start (Sunday).
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    result = get_start_of_week(dt, start_of_week=6)
    assert result == datetime(2023, 6, 4, 14, 30, 45)


def test_get_start_of_week_month_boundary() -> None:
    """
    Test case 3: get_start_of_week handles month boundary correctly.
    """
    dt = datetime(2023, 5, 1, 8, 0)
    result = get_start_of_week(dt)
    assert result == datetime(2023, 5, 1, 8, 0)


def test_get_start_of_week_year_boundary() -> None:
    """
    Test case 4: get_start_of_week handles year boundary correctly.
    """
    dt = datetime(2023, 1, 1, 0, 0)
    result = get_start_of_week(dt)
    assert result == datetime(2022, 12, 26, 0, 0)


def test_get_start_of_week_type_error() -> None:
    """
    Test case 5: get_start_of_week raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_start_of_week("2023-06-07")
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_start_of_week(123)


def test_get_start_of_week_value_error() -> None:
    """
    Test case 6: get_start_of_week raises ValueError for invalid start_of_week argument.
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    with pytest.raises(
        ValueError, match="start_of_week must be an integer between 0 and 6"
    ):
        get_start_of_week(dt, start_of_week=7)
