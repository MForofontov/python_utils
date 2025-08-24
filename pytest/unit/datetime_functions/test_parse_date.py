import pytest
from datetime import datetime, date
from datetime_functions.parse_date import parse_date


def test_parse_date_with_default_formats() -> None:
    """
    Test parse_date function with default date formats.
    """
    # Test case 1: Standard date format
    result: date = parse_date('2023-01-15')
    assert isinstance(result, date)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15


def test_parse_date_with_datetime_formats() -> None:
    """
    Test parse_date function with datetime formats returns datetime objects.
    """
    # Test case 2: Datetime format
    result: datetime = parse_date('2023-01-15 14:30:00')
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15
    assert result.hour == 14
    assert result.minute == 30


def test_parse_date_with_custom_formats() -> None:
    """
    Test parse_date function with custom format list.
    """
    # Test case 3: Custom format
    custom_formats: list[str] = ['%d.%m.%Y']
    result: date = parse_date('15.01.2023', formats=custom_formats)
    assert isinstance(result, date)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 15


def test_parse_date_invalid_input_type() -> None:
    """
    Test parse_date function with invalid input type raises TypeError.
    """
    # Test case 4: Invalid input types
    with pytest.raises(TypeError):
        parse_date(123)
    
    with pytest.raises(TypeError):
        parse_date(None)
    
    with pytest.raises(TypeError):
        parse_date(['2023-01-15'])


def test_parse_date_empty_string() -> None:
    """
    Test parse_date function with empty string raises ValueError.
    """
    # Test case 5: Empty string
    with pytest.raises(ValueError):
        parse_date('')
    
    with pytest.raises(ValueError):
        parse_date('   ')


def test_parse_date_unparseable_string() -> None:
    """
    Test parse_date function with unparseable string raises ValueError.
    """
    # Test case 6: Unparseable string
    with pytest.raises(ValueError):
        parse_date('not a date')
    
    with pytest.raises(ValueError):
        parse_date('2023-13-01')  # Invalid month
