from datetime import datetime

try:
    import pytz
    from python_utils.datetime_functions.convert_timezone import convert_timezone

    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    convert_timezone = None  # type: ignore

import pytest

pytestmark = pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.datetime]


def test_convert_timezone_naive_to_timezone() -> None:
    """
    Test case 1: Test convert_timezone function converting naive datetime to timezone.
    """
    naive_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: datetime = convert_timezone(naive_dt, "UTC")
    assert isinstance(result, datetime)
    assert result.tzinfo is not None
    assert result.hour == 12


def test_convert_timezone_aware_to_different_timezone() -> None:
    """
    Test case 2: Test convert_timezone function converting timezone-aware datetime to different timezone.
    """
    utc_tz = pytz.UTC
    utc_dt: datetime = utc_tz.localize(datetime(2023, 1, 15, 17, 0, 0))
    result: datetime = convert_timezone(utc_dt, "US/Eastern")
    assert isinstance(result, datetime)
    assert result.tzinfo is not None
    assert result.hour == 12  # UTC 17:00 = EST 12:00


def test_convert_timezone_with_pytz_objects() -> None:
    """
    Test case 3: Test convert_timezone function with pytz timezone objects.
    """
    utc_tz = pytz.UTC
    est_tz = pytz.timezone("US/Eastern")
    utc_dt: datetime = utc_tz.localize(datetime(2023, 1, 15, 17, 0, 0))
    result: datetime = convert_timezone(utc_dt, est_tz)
    assert isinstance(result, datetime)
    assert result.tzinfo is not None


def test_convert_timezone_with_from_timezone() -> None:
    """
    Test case 4: Test convert_timezone function with explicit from_timezone.
    """
    naive_dt: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: datetime = convert_timezone(naive_dt, "UTC", "US/Eastern")
    assert isinstance(result, datetime)
    assert result.tzinfo is not None


def test_convert_timezone_invalid_input_type() -> None:
    """
    Test case 5: Test convert_timezone function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        convert_timezone("2023-01-15", "UTC")

    with pytest.raises(TypeError):
        convert_timezone(123, "UTC")

    with pytest.raises(TypeError):
        convert_timezone(None, "UTC")


def test_convert_timezone_invalid_timezone_name() -> None:
    """
    Test case 6: Test convert_timezone function with invalid timezone name raises ValueError.
    """
    dt: datetime = datetime(2023, 1, 15, 12, 0, 0)

    with pytest.raises(ValueError):
        convert_timezone(dt, "Invalid/Timezone")

    with pytest.raises(ValueError):
        convert_timezone(dt, "UTC", "Invalid/Timezone")
