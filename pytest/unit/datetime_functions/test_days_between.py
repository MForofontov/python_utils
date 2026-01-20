from datetime import datetime

import pytest

try:
    import pytz
    from python_utils.datetime_functions.days_between import days_between
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    days_between = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.datetime,
    pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed"),
]


def test_days_between_positive_difference() -> None:
    """
    Test case 1: days_between with positive difference.
    """
    dt1 = datetime(2023, 1, 15, 0, 0, 0)
    dt2 = datetime(2023, 1, 20, 0, 0, 0)
    result = days_between(dt1, dt2)
    assert isinstance(result, int)
    assert result == 5


def test_days_between_negative_difference() -> None:
    """
    Test case 2: days_between with negative difference.
    """
    dt1 = datetime(2023, 1, 20, 0, 0, 0)
    dt2 = datetime(2023, 1, 15, 0, 0, 0)
    result = days_between(dt1, dt2)
    assert isinstance(result, int)
    assert result == -5


def test_days_between_same_dates() -> None:
    """
    Test case 3: days_between with same datetimes.
    """
    dt1 = datetime(2023, 1, 15, 0, 0, 0)
    dt2 = datetime(2023, 1, 15, 0, 0, 0)
    result = days_between(dt1, dt2)
    assert isinstance(result, int)
    assert result == 0


def test_days_between_with_datetime_objects() -> None:
    """
    Test case 4: days_between with datetime objects.
    """
    dt1 = datetime(2023, 1, 15, 10, 30, 0)
    dt2 = datetime(2023, 1, 18, 20, 45, 0)
    result = days_between(dt1, dt2)
    assert isinstance(result, int)
    assert result == 3


def test_days_between_cross_month() -> None:
    """
    Test case 5: days_between across month boundaries.
    """
    dt1 = datetime(2023, 1, 30, 0, 0, 0)
    dt2 = datetime(2023, 2, 2, 0, 0, 0)
    result = days_between(dt1, dt2)
    assert isinstance(result, int)
    assert result == 3

    # Removed: covered by test_days_between_type_error_on_non_datetime


def test_days_between_type_error_on_non_datetime() -> None:
    """
    Test case 6: days_between raises TypeError if either argument is not datetime.
    """
    dt2 = datetime(2023, 1, 20, 12, 0, 0)
    with pytest.raises(TypeError):
        days_between("2023-01-15", dt2)
    with pytest.raises(TypeError):
        days_between(dt2, "2023-01-20")
    with pytest.raises(TypeError):
        days_between(123, dt2)
    with pytest.raises(TypeError):
        days_between(dt2, None)
