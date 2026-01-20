from datetime import datetime

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.formatting]
from pyutils_collection.formatting_functions.format_date import format_date


def test_format_date_with_default_format() -> None:
    """
    Test case 1: format_date returns ISO format by default.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 0, 0, 0)
    result: str = format_date(test_datetime)
    assert isinstance(result, str)
    assert result == "2023-01-15"


def test_format_date_with_custom_format() -> None:
    """
    Test case 2: format_date returns string in custom format.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 0, 0, 0)
    result: str = format_date(test_datetime, "%d/%m/%Y")
    assert isinstance(result, str)
    assert result == "15/01/2023"


def test_format_datetime_object() -> None:
    """
    Test case 3: format_date works with datetime objects and custom format.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 14, 30, 0)
    result: str = format_date(test_datetime, "%Y-%m-%d %H:%M:%S")
    assert isinstance(result, str)
    assert result == "2023-01-15 14:30:00"


def test_format_date_human_readable() -> None:
    """
    Test case 4: format_date returns human-readable string format.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 0, 0, 0)
    result: str = format_date(test_datetime, "%B %d, %Y")
    assert isinstance(result, str)
    assert result == "January 15, 2023"


def test_format_date_invalid_input_type() -> None:
    """
    Test case 5: format_date raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError):
        format_date("2023-01-15")
    with pytest.raises(TypeError):
        format_date(123)
    with pytest.raises(TypeError):
        format_date(None)


def test_format_date_invalid_format_type() -> None:
    """
    Test case 6: format_date raises TypeError for invalid format argument types.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 0, 0, 0)
    with pytest.raises(TypeError):
        format_date(test_datetime, 123)
    with pytest.raises(TypeError):
        format_date(test_datetime, None)


def test_format_date_empty_format_string() -> None:
    """
    Test case 7: format_date raises ValueError for empty or whitespace format string.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 0, 0, 0)
    with pytest.raises(ValueError):
        format_date(test_datetime, "")
    with pytest.raises(ValueError):
        format_date(test_datetime, "   ")
