import pytest
from datetime import datetime, date
from datetime_functions.modify_months import modify_months


def test_modify_months_add_to_date_object() -> None:
    """
    Test modify_months function adding months to date object.
    """
    # Test case 1: Add months to date
    test_date: date = date(2023, 1, 15)
    result: date = modify_months(test_date, 3)
    assert isinstance(result, date)
    assert result == date(2023, 4, 15)


def test_modify_months_add_with_year_overflow() -> None:
    """
    Test modify_months function adding months with year overflow.
    """
    # Test case 2: Year overflow
    test_date: date = date(2023, 10, 15)
    result: date = modify_months(test_date, 6)
    assert isinstance(result, date)
    assert result == date(2024, 4, 15)


def test_modify_months_subtract_from_date_object() -> None:
    """
    Test modify_months function subtracting months from date object.
    """
    # Test case 3: Subtract months from date
    test_date: date = date(2023, 6, 15)
    result: date = modify_months(test_date, -3)
    assert isinstance(result, date)
    assert result == date(2023, 3, 15)


def test_modify_months_subtract_with_year_underflow() -> None:
    """
    Test modify_months function subtracting months with year underflow.
    """
    # Test case 4: Year underflow
    test_date: date = date(2023, 2, 15)
    result: date = modify_months(test_date, -6)
    assert isinstance(result, date)
    assert result == date(2022, 8, 15)


def test_modify_months_day_overflow() -> None:
    """
    Test modify_months function with day overflow handling.
    """
    # Test case 5: Day overflow (Jan 31 -> Feb 28/29)
    test_date: date = date(2023, 1, 31)
    result: date = modify_months(test_date, 1)
    assert isinstance(result, date)
    assert result == date(2023, 2, 28)  # Feb 31 doesn't exist
    
    # Test case 6: Day overflow going backwards (Mar 31 -> Feb 28/29)
    test_date2: date = date(2023, 3, 31)
    result2: date = modify_months(test_date2, -1)
    assert isinstance(result2, date)
    assert result2 == date(2023, 2, 28)


def test_modify_months_leap_year_handling() -> None:
    """
    Test modify_months function with leap year handling.
    """
    # Test case 7: Leap year handling
    test_date: date = date(2020, 1, 31)
    result: date = modify_months(test_date, 1)
    assert isinstance(result, date)
    assert result == date(2020, 2, 29)  # 2020 is leap year


def test_modify_months_datetime_object() -> None:
    """
    Test modify_months function with datetime object.
    """
    # Test case 8: Datetime object
    test_datetime: datetime = datetime(2023, 1, 15, 12, 30, 0)
    result: datetime = modify_months(test_datetime, 2)
    assert isinstance(result, datetime)
    assert result.date() == date(2023, 3, 15)
    assert result.time() == test_datetime.time()


def test_modify_months_zero_change() -> None:
    """
    Test modify_months function with zero months.
    """
    # Test case 9: Zero change
    test_date: date = date(2023, 6, 15)
    result: date = modify_months(test_date, 0)
    assert isinstance(result, date)
    assert result == test_date


def test_modify_months_invalid_input_type() -> None:
    """
    Test modify_months function with invalid input type raises TypeError.
    """
    # Test case 10: Invalid input types
    with pytest.raises(TypeError):
        modify_months('2023-01-15', 3)
    
    with pytest.raises(TypeError):
        modify_months(123, 3)
    
    with pytest.raises(TypeError):
        modify_months(None, 3)


def test_modify_months_invalid_months_type() -> None:
    """
    Test modify_months function with invalid months type raises TypeError.
    """
    # Test case 11: Invalid months types
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(TypeError):
        modify_months(test_date, '3')
    
    with pytest.raises(TypeError):
        modify_months(test_date, 3.5)
    
    with pytest.raises(TypeError):
        modify_months(test_date, None)
