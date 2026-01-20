from datetime import datetime

import pytest

try:
    import pytz
    from python_utils.datetime_functions.get_days_in_month import get_days_in_month
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    get_days_in_month = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.datetime,
    pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed"),
]


def test_get_days_in_month_january() -> None:
    """
    Test case 1: get_days_in_month returns 31 for January.
    """
    test_datetime = datetime(2023, 1, 10, 0, 0, 0)
    result: int = get_days_in_month(test_datetime)
    assert isinstance(result, int)
    assert result == 31


def test_get_days_in_month_february_non_leap() -> None:
    """
    Test case 2: get_days_in_month returns 28 for February in a non-leap year.
    """
    test_datetime = datetime(2023, 2, 10, 0, 0, 0)
    result: int = get_days_in_month(test_datetime)
    assert isinstance(result, int)
    assert result == 28


def test_get_days_in_month_february_leap() -> None:
    """
    Test case 3: get_days_in_month returns 29 for February in a leap year.
    """
    test_datetime = datetime(2020, 2, 10, 0, 0, 0)
    result: int = get_days_in_month(test_datetime)
    assert isinstance(result, int)
    assert result == 29


def test_get_days_in_month_april() -> None:
    """
    Test case 4: get_days_in_month returns 30 for April.
    """
    test_datetime = datetime(2023, 4, 10, 0, 0, 0)
    result: int = get_days_in_month(test_datetime)
    assert isinstance(result, int)
    assert result == 30


def test_get_days_in_month_december() -> None:
    """
    Test case 5: get_days_in_month returns 31 for December.
    """
    test_datetime = datetime(2023, 12, 10, 0, 0, 0)
    result: int = get_days_in_month(test_datetime)
    assert isinstance(result, int)
    assert result == 31


def test_get_days_in_month_all_months() -> None:
    """
    Test case 6: get_days_in_month returns correct days for all months in a non-leap year.
    """
    expected_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month, expected in enumerate(expected_days, 1):
        dt = datetime(2023, month, 10, 0, 0, 0)
        result: int = get_days_in_month(dt)
        assert result == expected


def test_get_days_in_month_all_months_leap() -> None:
    """
    Test case 7: get_days_in_month returns correct days for all months in a leap year.
    """
    expected_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month, expected in enumerate(expected_days, 1):
        dt = datetime(2020, month, 10, 0, 0, 0)
        result: int = get_days_in_month(dt)
        assert result == expected


def test_get_days_in_month_from_datetime_object() -> None:
    """
    Test case 8: get_days_in_month returns 30 for June from a datetime object.
    """
    dt = datetime(2023, 6, 15, 0, 0, 0)
    result: int = get_days_in_month(dt)
    assert isinstance(result, int)
    assert result == 30  # June has 30 days


def test_get_days_in_month_invalid_input_type() -> None:
    """
    Test case 9: get_days_in_month raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError):
        get_days_in_month("not_a_datetime")
    with pytest.raises(TypeError):
        get_days_in_month(123)
    with pytest.raises(TypeError):
        get_days_in_month(None)
