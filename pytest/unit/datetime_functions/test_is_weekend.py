import pytest
from datetime import datetime, date
from datetime_functions.is_weekend import is_weekend


def test_is_weekend_monday() -> None:
    """
    Test is_weekend function with Monday.
    """
    # Test case 1: Monday (not weekend)
    test_date: date = date(2023, 6, 5)  # Monday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_tuesday() -> None:
    """
    Test is_weekend function with Tuesday.
    """
    # Test case 2: Tuesday (not weekend)
    test_date: date = date(2023, 6, 6)  # Tuesday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_wednesday() -> None:
    """
    Test is_weekend function with Wednesday.
    """
    # Test case 3: Wednesday (not weekend)
    test_date: date = date(2023, 6, 7)  # Wednesday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_thursday() -> None:
    """
    Test is_weekend function with Thursday.
    """
    # Test case 4: Thursday (not weekend)
    test_date: date = date(2023, 6, 8)  # Thursday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_friday() -> None:
    """
    Test is_weekend function with Friday.
    """
    # Test case 5: Friday (not weekend)
    test_date: date = date(2023, 6, 9)  # Friday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_saturday() -> None:
    """
    Test is_weekend function with Saturday.
    """
    # Test case 6: Saturday (weekend)
    test_date: date = date(2023, 6, 10)  # Saturday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_sunday() -> None:
    """
    Test is_weekend function with Sunday.
    """
    # Test case 7: Sunday (weekend)
    test_date: date = date(2023, 6, 11)  # Sunday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_with_datetime() -> None:
    """
    Test is_weekend function with datetime object.
    """
    # Test case 8: Datetime object for Saturday
    test_datetime: datetime = datetime(2023, 6, 10, 14, 30, 45)  # Saturday
    result: bool = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_with_datetime_sunday() -> None:
    """
    Test is_weekend function with datetime object for Sunday.
    """
    # Test case 9: Datetime object for Sunday
    test_datetime: datetime = datetime(2023, 6, 11, 23, 59, 59)  # Sunday
    result: bool = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_with_datetime_weekday() -> None:
    """
    Test is_weekend function with datetime object for weekday.
    """
    # Test case 10: Datetime object for weekday
    test_datetime: datetime = datetime(2023, 6, 7, 9, 0, 0)  # Wednesday
    result: bool = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_invalid_input_type() -> None:
    """
    Test is_weekend function with invalid input type raises TypeError.
    """
    # Test case 11: Invalid input types
    with pytest.raises(TypeError):
        is_weekend('2023-06-10')
    
    with pytest.raises(TypeError):
        is_weekend(123)
    
    with pytest.raises(TypeError):
        is_weekend(None)
