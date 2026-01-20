from datetime import date, datetime

import pytest

try:
    import pytz
    from pyutils_collection.datetime_functions.parse_date import parse_date
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    parse_date = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.datetime,
    pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed"),
]


def test_parse_date_with_default_formats() -> None:
    """
    Test case 1: Test parse_date function with default date formats.
    """
    result: date = parse_date("2023-01-15")
    assert isinstance(result, date)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15


def test_parse_date_with_datetime_formats() -> None:
    """
    Test case 2: Test parse_date function with datetime formats returns datetime objects.
    """
    result: datetime = parse_date("2023-01-15 14:30:00")
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15
    assert result.hour == 14
    assert result.minute == 30


def test_parse_date_with_custom_formats() -> None:
    """
    Test case 3: Test parse_date function with custom format list.
    """
    custom_formats: list[str] = ["%d.%m.%Y"]
    result: date = parse_date("15.01.2023", formats=custom_formats)
    assert isinstance(result, date)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15


def test_parse_date_invalid_input_type() -> None:
    """
    Test case 4: Test parse_date function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        parse_date(123)

    with pytest.raises(TypeError):
        parse_date(None)

    with pytest.raises(TypeError):
        parse_date(["2023-01-15"])


def test_parse_date_empty_string() -> None:
    """
    Test case 5: Test parse_date function with empty string raises ValueError.
    """
    with pytest.raises(ValueError):
        parse_date("")

    with pytest.raises(ValueError):
        parse_date("   ")


def test_parse_date_unparseable_string() -> None:
    """
    Test case 6: Test parse_date function with unparseable string raises ValueError.
    """
    with pytest.raises(ValueError):
        parse_date("not a date")

    with pytest.raises(ValueError):
        parse_date("2023-13-01")  # Invalid month
