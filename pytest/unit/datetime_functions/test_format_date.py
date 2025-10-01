from datetime import date, datetime

import pytest
from datetime_functions.format_date import format_date


def test_format_date_with_default_format() -> None:
    """
    Test case 1: Test format_date function with default format string.
    """
    test_date: date = date(2023, 1, 15)
    result: str = format_date(test_date)
    assert isinstance(result, str)
    assert result == "2023-01-15"


def test_format_date_with_custom_format() -> None:
    """
    Test case 2: Test format_date function with custom format string.
    """
    test_date: date = date(2023, 1, 15)
    result: str = format_date(test_date, "%d/%m/%Y")
    assert isinstance(result, str)
    assert result == "15/01/2023"


def test_format_datetime_object() -> None:
    """
    Test case 3: Test format_date function with datetime object.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 14, 30, 0)
    result: str = format_date(test_datetime, "%Y-%m-%d %H:%M:%S")
    assert isinstance(result, str)
    assert result == "2023-01-15 14:30:00"


def test_format_date_human_readable() -> None:
    """
    Test case 4: Test format_date function with human-readable format.
    """
    test_date: date = date(2023, 1, 15)
    result: str = format_date(test_date, "%B %d, %Y")
    assert isinstance(result, str)
    assert result == "January 15, 2023"


def test_format_date_invalid_input_type() -> None:
    """
    Test case 5: Test format_date function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        format_date("2023-01-15")

    with pytest.raises(TypeError):
        format_date(123)

    with pytest.raises(TypeError):
        format_date(None)


def test_format_date_invalid_format_type() -> None:
    """
    Test case 6: Test format_date function with invalid format type raises TypeError.
    """
    test_date: date = date(2023, 1, 15)

    with pytest.raises(TypeError):
        format_date(test_date, 123)

    with pytest.raises(TypeError):
        format_date(test_date, None)


def test_format_date_empty_format_string() -> None:
    """
    Test case 7: Test format_date function with empty format string raises ValueError.
    """
    test_date: date = date(2023, 1, 15)

    with pytest.raises(ValueError):
        format_date(test_date, "")

    with pytest.raises(ValueError):
        format_date(test_date, "   ")


