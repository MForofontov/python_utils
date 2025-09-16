from datetime import date, datetime

import pytest
from datetime_functions.get_week_number import get_week_number


def test_get_week_number_first_week() -> None:
    """
    Test case 1: Test get_week_number function with first week of year.
    """
    test_date: date = date(2023, 1, 2)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 1


def test_get_week_number_january_1st() -> None:
    """
    Test case 2: Test get_week_number function with January 1st.
    """
    test_date: date = date(2023, 1, 1)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 52


def test_get_week_number_mid_year() -> None:
    """
    Test case 3: Test get_week_number function with mid-year date.
    """
    test_date: date = date(2023, 6, 15)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 24


def test_get_week_number_last_week() -> None:
    """
    Test case 4: Test get_week_number function with last week of year.
    """
    test_date: date = date(2023, 12, 31)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 52


def test_get_week_number_leap_year() -> None:
    """
    Test case 5: Test get_week_number function with leap year date.
    """
    test_date: date = date(2020, 2, 29)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 9


def test_get_week_number_with_datetime() -> None:
    """
    Test case 6: Test get_week_number function with datetime object.
    """
    test_datetime: datetime = datetime(2023, 6, 15, 14, 30, 45)
    result: int = get_week_number(test_datetime)
    assert isinstance(result, int)
    assert result == 24


def test_get_week_number_week_53() -> None:
    """
    Test case 7: Test get_week_number function with year having 53 weeks.
    """
    test_date: date = date(2020, 12, 31)  # Thursday
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 53


def test_get_week_number_different_years() -> None:
    """
    Test case 8: Test get_week_number function with different years.
    """
    test_date_2022: date = date(2022, 6, 15)
    test_date_2023: date = date(2023, 6, 15)

    result_2022: int = get_week_number(test_date_2022)
    result_2023: int = get_week_number(test_date_2023)

    assert isinstance(result_2022, int)
    assert isinstance(result_2023, int)
    assert result_2022 == 24
    assert result_2023 == 24


def test_get_week_number_monday_start() -> None:
    """
    Test case 9: Test get_week_number function with Monday (start of ISO week).
    """
    test_date: date = date(2023, 6, 5)  # Monday
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 23


def test_get_week_number_invalid_input_type() -> None:
    """
    Test case 10: Test get_week_number function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_week_number("2023-06-15")

    with pytest.raises(TypeError):
        get_week_number(123)

    with pytest.raises(TypeError):
        get_week_number(None)
