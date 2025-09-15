import pytest
from datetime import datetime, date
from datetime_functions.is_weekend import is_weekend


def test_is_weekend_monday() -> None:
    """
    Test case 1: Test is_weekend function with Monday.
    """
    test_date: date = date(2023, 6, 5)  # Monday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_tuesday() -> None:
    """
    Test case 2: Test is_weekend function with Tuesday.
    """
    test_date: date = date(2023, 6, 6)  # Tuesday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_wednesday() -> None:
    """
    Test case 3: Test is_weekend function with Wednesday.
    """
    test_date: date = date(2023, 6, 7)  # Wednesday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_thursday() -> None:
    """
    Test case 4: Test is_weekend function with Thursday.
    """
    test_date: date = date(2023, 6, 8)  # Thursday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_friday() -> None:
    """
    Test case 5: Test is_weekend function with Friday.
    """
    test_date: date = date(2023, 6, 9)  # Friday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_saturday() -> None:
    """
    Test case 6: Test is_weekend function with Saturday.
    """
    test_date: date = date(2023, 6, 10)  # Saturday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_sunday() -> None:
    """
    Test case 7: Test is_weekend function with Sunday.
    """
    test_date: date = date(2023, 6, 11)  # Sunday
    result: bool = is_weekend(test_date)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_with_datetime() -> None:
    """
    Test case 8: Test is_weekend function with datetime object.
    """
    test_datetime: datetime = datetime(2023, 6, 10, 14, 30, 45)  # Saturday
    result: bool = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_with_datetime_sunday() -> None:
    """
    Test case 9: Test is_weekend function with datetime object for Sunday.
    """
    test_datetime: datetime = datetime(2023, 6, 11, 23, 59, 59)  # Sunday
    result: bool = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is True


def test_is_weekend_with_datetime_weekday() -> None:
    """
    Test case 10: Test is_weekend function with datetime object for weekday.
    """
    test_datetime: datetime = datetime(2023, 6, 7, 9, 0, 0)  # Wednesday
    result: bool = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False


def test_is_weekend_invalid_input_type() -> None:
    """
    Test case 11: Test is_weekend function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        is_weekend("2023-06-10")

    with pytest.raises(TypeError):
        is_weekend(123)

    with pytest.raises(TypeError):
        is_weekend(None)
