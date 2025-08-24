import pytest
from datetime import datetime, date
from datetime_functions.modify_years import modify_years


def test_modify_years_add_to_date_object() -> None:
    """
    Test modify_years function adding years to date object.
    """
    # Test case 1: Add years to date
    test_date: date = date(2023, 1, 15)
    result: date = modify_years(test_date, 2)
    assert isinstance(result, date)
    assert result == date(2025, 1, 15)


def test_modify_years_add_to_datetime_object() -> None:
    """
    Test modify_years function adding years to datetime object.
    """
    # Test case 2: Add years to datetime
    test_datetime: datetime = datetime(2023, 1, 15, 12, 30, 0)
    result: datetime = modify_years(test_datetime, 3)
    assert isinstance(result, datetime)
    assert result.date() == date(2026, 1, 15)
    assert result.time() == test_datetime.time()


def test_modify_years_subtract_from_date_object() -> None:
    """
    Test modify_years function subtracting years from date object.
    """
    # Test case 3: Subtract years from date
    test_date: date = date(2023, 1, 15)
    result: date = modify_years(test_date, -3)
    assert isinstance(result, date)
    assert result == date(2020, 1, 15)


def test_modify_years_subtract_from_datetime_object() -> None:
    """
    Test modify_years function subtracting years from datetime object.
    """
    # Test case 4: Subtract years from datetime
    test_datetime: datetime = datetime(2023, 6, 15, 12, 30, 0)
    result: datetime = modify_years(test_datetime, -2)
    assert isinstance(result, datetime)
    assert result.date() == date(2021, 6, 15)
    assert result.time() == test_datetime.time()


def test_modify_years_zero_change() -> None:
    """
    Test modify_years function with zero years.
    """
    # Test case 5: Zero change
    test_date: date = date(2023, 1, 15)
    result: date = modify_years(test_date, 0)
    assert isinstance(result, date)
    assert result == test_date


def test_modify_years_leap_year_handling_add() -> None:
    """
    Test modify_years function with leap year Feb 29 handling when adding.
    """
    # Test case 6: Leap year Feb 29 -> non-leap year Feb 28
    test_date: date = date(2020, 2, 29)  # 2020 is leap year
    result: date = modify_years(test_date, 1)
    assert isinstance(result, date)
    assert result == date(2021, 2, 28)  # 2021 is not leap year


def test_modify_years_leap_year_handling_subtract() -> None:
    """
    Test modify_years function with leap year Feb 29 handling when subtracting.
    """
    # Test case 7: Leap year Feb 29 -> non-leap year Feb 28
    test_date: date = date(2020, 2, 29)  # 2020 is leap year
    result: date = modify_years(test_date, -1)
    assert isinstance(result, date)
    assert result == date(2019, 2, 28)  # 2019 is not leap year


def test_modify_years_leap_to_leap() -> None:
    """
    Test modify_years function from leap year to leap year.
    """
    # Test case 8: Leap year to leap year
    test_date: date = date(2020, 2, 29)
    result_add: date = modify_years(test_date, 4)
    assert result_add == date(2024, 2, 29)  # 2024 is also leap year
    
    test_date2: date = date(2024, 2, 29)
    result_subtract: date = modify_years(test_date2, -4)
    assert result_subtract == date(2020, 2, 29)  # 2020 is also leap year


def test_modify_years_invalid_input_type() -> None:
    """
    Test modify_years function with invalid input type raises TypeError.
    """
    # Test case 9: Invalid input types
    with pytest.raises(TypeError):
        modify_years('2023-01-15', 2)
    
    with pytest.raises(TypeError):
        modify_years(123, 2)
    
    with pytest.raises(TypeError):
        modify_years(None, 2)


def test_modify_years_invalid_years_type() -> None:
    """
    Test modify_years function with invalid years type raises TypeError.
    """
    # Test case 10: Invalid years types
    test_date: date = date(2023, 1, 15)
    
    with pytest.raises(TypeError):
        modify_years(test_date, '2')
    
    with pytest.raises(TypeError):
        modify_years(test_date, 2.5)
    
    with pytest.raises(TypeError):
        modify_years(test_date, None)
