import pytest
from datetime import datetime, date
from datetime_functions.modify_days import modify_days


def test_modify_days_add_to_date_object() -> None:
    """
    Test modify_days function adding days to date object.
    """
    # Test case 1: Add days to date
    test_date: date = date(2023, 1, 15)
    result: date = modify_days(test_date, 10)
    assert isinstance(result, date)
    assert result == date(2023, 1, 25)


def test_modify_days_add_to_datetime_object() -> None:
    """
    Test modify_days function adding days to datetime object.
    """
    # Test case 2: Add days to datetime
    test_datetime: datetime = datetime(2023, 1, 15, 12, 30, 0)
    result: datetime = modify_days(test_datetime, 5)
    assert isinstance(result, datetime)
    assert result.date() == date(2023, 1, 20)
    assert result.time() == test_datetime.time()


def test_modify_days_subtract_from_date_object() -> None:
    """
    Test modify_days function subtracting days from date object.
    """
    # Test case 3: Subtract days from date
    test_date: date = date(2023, 1, 20)
    result: date = modify_days(test_date, -5)
    assert isinstance(result, date)
    assert result == date(2023, 1, 15)


def test_modify_days_subtract_from_datetime_object() -> None:
    """
    Test modify_days function subtracting days from datetime object.
    """
    # Test case 4: Subtract days from datetime
    test_datetime: datetime = datetime(2023, 1, 20, 12, 30, 0)
    result: datetime = modify_days(test_datetime, -3)
    assert isinstance(result, datetime)
    assert result.date() == date(2023, 1, 17)
    assert result.time() == test_datetime.time()


def test_modify_days_zero_change() -> None:
    """
    Test modify_days function with zero days.
    """
    # Test case 5: Zero change
    test_date: date = date(2023, 1, 15)
    result: date = modify_days(test_date, 0)
    assert isinstance(result, date)
    assert result == test_date


def test_modify_days_month_boundary() -> None:
    """
    Test modify_days function crossing month boundaries.
    """
    # Test case 6: Month overflow and underflow
    test_date: date = date(2023, 1, 30)
    result_add: date = modify_days(test_date, 5)
    assert result_add == date(2023, 2, 4)
    
    test_date2: date = date(2023, 2, 3)
    result_subtract: date = modify_days(test_date2, -5)
    assert result_subtract == date(2023, 1, 29)


def test_modify_days_invalid_input_type() -> None:
    """
    Test modify_days function with invalid input type raises TypeError.
    """
    # Test case 7: Invalid input types
    with pytest.raises(TypeError):
        modify_days('2023-01-15', 5)
    
    with pytest.raises(TypeError):
        modify_days(123, 5)
    
    with pytest.raises(TypeError):
        modify_days(None, 5)


def test_modify_days_invalid_days_type() -> None:
    """
    Test modify_days function with invalid days type raises TypeError.
    """
    # Test case 8: Invalid days types
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(TypeError):
        modify_days(test_date, '5')
    
    with pytest.raises(TypeError):
        modify_days(test_date, 5.5)
    
    with pytest.raises(TypeError):
        modify_days(test_date, None)
