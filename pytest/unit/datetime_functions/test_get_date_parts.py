import pytest
from datetime import datetime, date
from datetime_functions.get_date_parts import get_date_parts


def test_get_date_parts_basic() -> None:
    """
    Test get_date_parts function with basic date.
    """
    # Test case 1: Basic date parts
    test_date: date = date(2023, 6, 15)
    result: dict = get_date_parts(test_date)
    assert isinstance(result, dict)
    assert result['year'] == 2023
    assert result['month'] == 6
    assert result['day'] == 15
    assert result['weekday'] == 3  # Thursday (0=Monday)
    assert isinstance(result['day_of_year'], int)


def test_get_date_parts_with_datetime() -> None:
    """
    Test get_date_parts function with datetime object.
    """
    # Test case 2: Datetime object
    test_datetime: datetime = datetime(2023, 12, 25, 15, 30, 45)
    result: dict = get_date_parts(test_datetime)
    assert isinstance(result, dict)
    assert result['year'] == 2023
    assert result['month'] == 12
    assert result['day'] == 25
    assert result['weekday'] == 0  # Monday (0=Monday)
    assert isinstance(result['day_of_year'], int)


def test_get_date_parts_january_first() -> None:
    """
    Test get_date_parts function with January 1st.
    """
    # Test case 3: January 1st
    test_date: date = date(2023, 1, 1)
    result: dict = get_date_parts(test_date)
    assert isinstance(result, dict)
    assert result['year'] == 2023
    assert result['month'] == 1
    assert result['day'] == 1
    assert result['day_of_year'] == 1


def test_get_date_parts_december_last() -> None:
    """
    Test get_date_parts function with December 31st.
    """
    # Test case 4: December 31st
    test_date: date = date(2023, 12, 31)
    result: dict = get_date_parts(test_date)
    assert isinstance(result, dict)
    assert result['year'] == 2023
    assert result['month'] == 12
    assert result['day'] == 31
    assert result['day_of_year'] == 365  # 2023 is not a leap year


def test_get_date_parts_leap_year() -> None:
    """
    Test get_date_parts function with leap year date.
    """
    # Test case 5: Leap year
    test_date: date = date(2020, 12, 31)  # 2020 is leap year
    result: dict = get_date_parts(test_date)
    assert isinstance(result, dict)
    assert result['year'] == 2020
    assert result['month'] == 12
    assert result['day'] == 31
    assert result['day_of_year'] == 366  # Leap year has 366 days


def test_get_date_parts_weekday_values() -> None:
    """
    Test get_date_parts function weekday values are correct.
    """
    # Test case 6: Known weekdays
    # Monday 2023-06-12
    monday: date = date(2023, 6, 12)
    result_mon: dict = get_date_parts(monday)
    assert result_mon['weekday'] == 0
    
    # Sunday 2023-06-18
    sunday: date = date(2023, 6, 18)
    result_sun: dict = get_date_parts(sunday)
    assert result_sun['weekday'] == 6


def test_get_date_parts_all_keys_present() -> None:
    """
    Test get_date_parts function returns all expected keys.
    """
    # Test case 7: All keys present
    test_date: date = date(2023, 6, 15)
    result: dict = get_date_parts(test_date)
    expected_keys = {'year', 'month', 'day', 'weekday', 'day_of_year'}
    assert set(result.keys()) == expected_keys


def test_get_date_parts_invalid_input_type() -> None:
    """
    Test get_date_parts function with invalid input type raises TypeError.
    """
    # Test case 8: Invalid input types
    with pytest.raises(TypeError):
        get_date_parts('2023-06-15')
    
    with pytest.raises(TypeError):
        get_date_parts(123)
    
    with pytest.raises(TypeError):
        get_date_parts(None)
