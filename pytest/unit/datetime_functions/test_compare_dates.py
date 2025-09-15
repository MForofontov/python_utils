import pytest
from datetime import datetime, date
from datetime_functions.compare_dates import compare_dates


def test_compare_dates_first_earlier() -> None:
    """
    Test case 1: Test compare_dates function when first date is earlier.
    """
    date1: date = date(2023, 1, 15)
    date2: date = date(2023, 2, 15)
    result: int = compare_dates(date1, date2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_first_later() -> None:
    """
    Test case 2: Test compare_dates function when first date is later.
    """
    date1: date = date(2023, 2, 15)
    date2: date = date(2023, 1, 15)
    result: int = compare_dates(date1, date2)
    assert isinstance(result, int)
    assert result == 1


def test_compare_dates_equal() -> None:
    """
    Test case 3: Test compare_dates function when dates are equal.
    """
    date1: date = date(2023, 1, 15)
    date2: date = date(2023, 1, 15)
    result: int = compare_dates(date1, date2)
    assert isinstance(result, int)
    assert result == 0


def test_compare_dates_with_datetime_objects() -> None:
    """
    Test case 4: Test compare_dates function with datetime objects.
    """
    dt1: datetime = datetime(2023, 1, 15, 10, 30, 0)
    dt2: datetime = datetime(2023, 1, 15, 15, 45, 0)
    result: int = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == -1  # Earlier time


def test_compare_dates_mixed_types() -> None:
    """
    Test case 5: Test compare_dates function with mixed date and datetime objects.
    """
    date1: date = date(2023, 1, 15)
    dt2: datetime = datetime(2023, 1, 16, 12, 0, 0)
    result: int = compare_dates(date1, dt2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_different_years() -> None:
    """
    Test case 6: Test compare_dates function with different years.
    """
    date1: date = date(2022, 12, 31)
    date2: date = date(2023, 1, 1)
    result: int = compare_dates(date1, date2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_same_date_different_time() -> None:
    """
    Test case 7: Test compare_dates function with same date but different times.
    """
    dt1: datetime = datetime(2023, 1, 15, 9, 0, 0)
    dt2: datetime = datetime(2023, 1, 15, 17, 0, 0)
    result: int = compare_dates(dt1, dt2)
    assert isinstance(result, int)
    assert result == -1


def test_compare_dates_invalid_input_type() -> None:
    """
    Test case 8: Test compare_dates function with invalid input type raises TypeError.
    """
    test_date: date = date(2023, 1, 15)

    with pytest.raises(TypeError):
        compare_dates("2023-01-15", test_date)

    with pytest.raises(TypeError):
        compare_dates(test_date, "2023-01-16")

    with pytest.raises(TypeError):
        compare_dates(123, test_date)

    with pytest.raises(TypeError):
        compare_dates(test_date, None)
