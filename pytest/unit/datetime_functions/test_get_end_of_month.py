from datetime import datetime

import pytest
from datetime_functions.get_end_of_month import get_end_of_month


def test_get_end_of_month_january() -> None:
    """
    Test case 1: get_end_of_month returns last day of January.
    """
    dt = datetime(2023, 1, 15, 8, 0, 0)
    result = get_end_of_month(dt)
    assert result == datetime(2023, 1, 31, 8, 0, 0)


def test_get_end_of_month_february_non_leap() -> None:
    """
    Test case 2: get_end_of_month returns last day of February in a non-leap year.
    """
    dt = datetime(2023, 2, 10, 12, 30)
    result = get_end_of_month(dt)
    assert result == datetime(2023, 2, 28, 12, 30)


def test_get_end_of_month_february_leap() -> None:
    """
    Test case 3: get_end_of_month returns last day of February in a leap year.
    """
    dt = datetime(2020, 2, 15, 23, 59, 59)
    result = get_end_of_month(dt)
    assert result == datetime(2020, 2, 29, 23, 59, 59)


def test_get_end_of_month_april() -> None:
    """
    Test case 4: get_end_of_month returns last day of April.
    """
    dt = datetime(2023, 4, 5, 0, 0, 1)
    result = get_end_of_month(dt)
    assert result == datetime(2023, 4, 30, 0, 0, 1)


def test_get_end_of_month_december() -> None:
    """
    Test case 5: get_end_of_month returns last day of December.
    """
    dt = datetime(2023, 12, 1, 15, 45)
    result = get_end_of_month(dt)
    assert result == datetime(2023, 12, 31, 15, 45)


def test_get_end_of_month_first_day() -> None:
    """
    Test case 6: get_end_of_month returns last day for a date on the first of the month.
    """
    dt = datetime(2023, 5, 1, 6, 0)
    result = get_end_of_month(dt)
    assert result == datetime(2023, 5, 31, 6, 0)


def test_get_end_of_month_type_error() -> None:
    """
    Test case 7: get_end_of_month raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_end_of_month("2023-02-15")
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_end_of_month(123)
