import pytest
from datetime import datetime, date
from datetime_functions.modify_weeks import modify_weeks


def test_modify_weeks_add_to_date_object() -> None:
    """
    Test case 1: Test modify_weeks function adding weeks to date object.
    """
    test_date: date = date(2023, 1, 15)
    result: date = modify_weeks(test_date, 2)
    assert isinstance(result, date)
    assert result == date(2023, 1, 29)


def test_modify_weeks_add_to_datetime_object() -> None:
    """
    Test case 2: Test modify_weeks function adding weeks to datetime object.
    """
    test_datetime: datetime = datetime(2023, 1, 15, 12, 30, 0)
    result: datetime = modify_weeks(test_datetime, 3)
    assert isinstance(result, datetime)
    assert result.date() == date(2023, 2, 5)
    assert result.time() == test_datetime.time()


def test_modify_weeks_subtract_from_date_object() -> None:
    """
    Test case 3: Test modify_weeks function subtracting weeks from date object.
    """
    test_date: date = date(2023, 2, 15)
    result: date = modify_weeks(test_date, -2)
    assert isinstance(result, date)
    assert result == date(2023, 2, 1)


def test_modify_weeks_subtract_from_datetime_object() -> None:
    """
    Test case 4: Test modify_weeks function subtracting weeks from datetime object.
    """
    test_datetime: datetime = datetime(2023, 2, 15, 12, 30, 0)
    result: datetime = modify_weeks(test_datetime, -1)
    assert isinstance(result, datetime)
    assert result.date() == date(2023, 2, 8)
    assert result.time() == test_datetime.time()


def test_modify_weeks_zero_change() -> None:
    """
    Test case 5: Test modify_weeks function with zero weeks.
    """
    test_date: date = date(2023, 1, 15)
    result: date = modify_weeks(test_date, 0)
    assert isinstance(result, date)
    assert result == test_date


def test_modify_weeks_month_boundary() -> None:
    """
    Test case 6: Test modify_weeks function crossing month boundaries.
    """
    test_date: date = date(2023, 1, 25)
    result_add: date = modify_weeks(test_date, 2)
    assert result_add == date(2023, 2, 8)

    test_date2: date = date(2023, 2, 5)
    result_subtract: date = modify_weeks(test_date2, -2)
    assert result_subtract == date(2023, 1, 22)


def test_modify_weeks_invalid_input_type() -> None:
    """
    Test case 7: Test modify_weeks function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        modify_weeks("2023-01-15", 2)

    with pytest.raises(TypeError):
        modify_weeks(123, 2)

    with pytest.raises(TypeError):
        modify_weeks(None, 2)


def test_modify_weeks_invalid_weeks_type() -> None:
    """
    Test case 8: Test modify_weeks function with invalid weeks type raises TypeError.
    """
    test_date: date = date(2023, 1, 15)

    with pytest.raises(TypeError):
        modify_weeks(test_date, "2")

    with pytest.raises(TypeError):
        modify_weeks(test_date, 2.5)

    with pytest.raises(TypeError):
        modify_weeks(test_date, None)
