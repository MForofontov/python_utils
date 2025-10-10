from datetime import datetime

import pytest
from datetime_functions.get_end_of_week import get_end_of_week


def test_get_end_of_week_default() -> None:
    """
    Test case 1: get_end_of_week returns correct end of week for default start (Sunday).
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    result = get_end_of_week(dt)
    assert result == datetime(2023, 6, 11, 14, 30, 45)


def test_get_end_of_week_custom_start() -> None:
    """
    Test case 2: get_end_of_week returns correct end of week for custom start (Saturday).
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    result = get_end_of_week(dt, start_of_week=6)
    assert result == datetime(2023, 6, 10, 14, 30, 45)


def test_get_end_of_week_month_boundary() -> None:
    """
    Test case 3: get_end_of_week handles month boundary correctly.
    """
    dt = datetime(2023, 4, 28, 9, 0)
    result = get_end_of_week(dt)
    assert result == datetime(2023, 4, 30, 9, 0)


def test_get_end_of_week_year_boundary() -> None:
    """
    Test case 4: get_end_of_week handles year boundary correctly.
    """
    dt = datetime(2022, 12, 30, 23, 59)
    result = get_end_of_week(dt)
    assert result == datetime(2023, 1, 1, 23, 59)


def test_get_end_of_week_type_error() -> None:
    """
    Test case 5: get_end_of_week raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_end_of_week("2023-06-07")
    with pytest.raises(TypeError, match="date_obj must be a datetime"):
        get_end_of_week(123)


def test_get_end_of_week_value_error() -> None:
    """
    Test case 6: get_end_of_week raises ValueError for invalid start_of_week argument.
    """
    dt = datetime(2023, 6, 7, 14, 30, 45)
    with pytest.raises(
        ValueError, match="start_of_week must be an integer between 0 and 6"
    ):
        get_end_of_week(dt, start_of_week=7)
