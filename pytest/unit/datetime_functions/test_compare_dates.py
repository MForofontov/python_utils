from datetime import datetime

import pytest
from datetime_functions.compare_dates import compare_dates


def test_compare_dates_first_earlier() -> None:
    """
    Test case 1: compare_dates returns -1 when first datetime is earlier.
    """
    dt1 = datetime(2023, 1, 15, 10, 0, 0)
    dt2 = datetime(2023, 2, 15, 10, 0, 0)
    result = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_first_later() -> None:
    """
    Test case 2: compare_dates returns 1 when first datetime is later.
    """
    dt1 = datetime(2023, 2, 15, 10, 0, 0)
    dt2 = datetime(2023, 1, 15, 10, 0, 0)
    result = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == 1


def test_compare_dates_equal() -> None:
    """
    Test case 3: compare_dates returns 0 when datetimes are equal.
    """
    dt1 = datetime(2023, 1, 15, 10, 0, 0)
    dt2 = datetime(2023, 1, 15, 10, 0, 0)
    result = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == 0


def test_compare_dates_with_datetime_objects() -> None:
    """
    Test case 4: compare_dates returns -1 for earlier time on same day.
    """
    dt1 = datetime(2023, 1, 15, 10, 30, 0)
    dt2 = datetime(2023, 1, 15, 15, 45, 0)
    result = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_different_years() -> None:
    """
    Test case 5: compare_dates returns -1 for earlier year.
    """
    dt1 = datetime(2022, 12, 31, 23, 59, 59)
    dt2 = datetime(2023, 1, 1, 0, 0, 0)
    result = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_same_date_different_time() -> None:
    """
    Test case 6: compare_dates returns -1 for earlier time on same date.
    """
    dt1 = datetime(2023, 1, 15, 9, 0, 0)
    dt2 = datetime(2023, 1, 15, 17, 0, 0)
    result = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_type_error_on_non_datetime() -> None:
    """
    Test case 7: compare_dates raises TypeError if either argument is not datetime.
    """
    dt = datetime(2023, 1, 16, 12, 0, 0)
    with pytest.raises(TypeError):
        compare_dates("2023-01-15", dt)
    with pytest.raises(TypeError):
        compare_dates(dt, "2023-01-16")
    with pytest.raises(TypeError):
        compare_dates(123, dt)
    with pytest.raises(TypeError):
        compare_dates(dt, None)
