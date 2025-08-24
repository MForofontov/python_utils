import pytest
from datetime import datetime, date
from datetime_functions.format_date import format_date


def test_format_date_with_default_format() -> None:
    """
    Test format_date function with default format string.
    """
    # Test case 1: Date object with default format
    test_date: date = date(2023, 1, 15)
    result: str = format_date(test_date)
    assert isinstance(result, str)
    assert result == '2023-01-15'


def test_format_date_with_custom_format() -> None:
    """
    Test format_date function with custom format string.
    """
    # Test case 2: Date object with custom format
    test_date: date = date(2023, 1, 15)
    result: str = format_date(test_date, '%d/%m/%Y')
    assert isinstance(result, str)
    assert result == '15/01/2023'


def test_format_datetime_object() -> None:
    """
    Test format_date function with datetime object.
    """
    # Test case 3: Datetime object
    test_datetime: datetime = datetime(2023, 1, 15, 14, 30, 0)
    result: str = format_date(test_datetime, '%Y-%m-%d %H:%M:%S')
    assert isinstance(result, str)
    assert result == '2023-01-15 14:30:00'


def test_format_date_human_readable() -> None:
    """
    Test format_date function with human-readable format.
    """
    # Test case 4: Human-readable format
    test_date: date = date(2023, 1, 15)
    result: str = format_date(test_date, '%B %d, %Y')
    assert isinstance(result, str)
    assert result == 'January 15, 2023'


def test_format_date_invalid_input_type() -> None:
    """
    Test format_date function with invalid input type raises TypeError.
    """
    # Test case 5: Invalid input types
    with pytest.raises(TypeError):
        format_date('2023-01-15')
    
    with pytest.raises(TypeError):
        format_date(123)
    
    with pytest.raises(TypeError):
        format_date(None)


def test_format_date_invalid_format_type() -> None:
    """
    Test format_date function with invalid format type raises TypeError.
    """
    # Test case 6: Invalid format types
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(TypeError):
        format_date(test_date, 123)
    
    with pytest.raises(TypeError):
        format_date(test_date, None)


def test_format_date_empty_format_string() -> None:
    """
    Test format_date function with empty format string raises ValueError.
    """
    # Test case 7: Empty format string
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(ValueError):
        format_date(test_date, '')
    
    with pytest.raises(ValueError):
        format_date(test_date, '   ')


def test_format_date_invalid_format_string() -> None:
    """
    Test format_date function with invalid format string raises ValueError.
    """
    # Test case 8: Invalid format string
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(ValueError):
        format_date(test_date, '%Z')  # Invalid format for date object
