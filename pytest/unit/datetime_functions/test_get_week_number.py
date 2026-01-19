from datetime import date, datetime

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.datetime]
from datetime_functions.get_week_number import get_week_number


def test_get_week_number_first_week() -> None:
    """
    Test case 1: get_week_number returns 1 for the first week of the year.
    """
    test_date: date = date(2023, 1, 2)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 1


def test_get_week_number_january_1st() -> None:
    """
    Test case 2: get_week_number returns 52 for January 1st (week overlaps previous year).
    """
    test_date: date = date(2023, 1, 1)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 52


def test_get_week_number_mid_year() -> None:
    """
    Test case 3: get_week_number returns correct week for a mid-year date.
    """
    test_date: date = date(2023, 6, 15)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 24


def test_get_week_number_last_week() -> None:
    """
    Test case 4: get_week_number returns 52 for the last week of the year.
    """
    test_date: date = date(2023, 12, 31)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 52


def test_get_week_number_leap_year() -> None:
    """
    Test case 5: get_week_number returns correct week for a leap year date.
    """
    test_date: date = date(2020, 2, 29)
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 9


def test_get_week_number_with_datetime() -> None:
    """
    Test case 6: get_week_number works with datetime objects.
    """
    test_datetime: datetime = datetime(2023, 6, 15, 14, 30, 45)
    result: int = get_week_number(test_datetime)
    assert isinstance(result, int)
    assert result == 24


def test_get_week_number_week_53() -> None:
    """
    Test case 7: get_week_number returns 53 for a year with 53 weeks.
    """
    test_date: date = date(2020, 12, 31)  # Thursday
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 53


def test_get_week_number_different_years() -> None:
    """
    Test case 8: get_week_number returns correct week for the same date in different years.
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
    Test case 9: get_week_number returns correct week for a Monday (start of ISO week).
    """
    test_date: date = date(2023, 6, 5)  # Monday
    result: int = get_week_number(test_date)
    assert isinstance(result, int)
    assert result == 23


def test_get_week_number_invalid_input_type() -> None:
    """
    Test case 10: get_week_number raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError):
        get_week_number("2023-06-15")

    with pytest.raises(TypeError):
        get_week_number(123)

    with pytest.raises(TypeError):
        get_week_number(None)
