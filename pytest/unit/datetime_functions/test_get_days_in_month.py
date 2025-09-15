import pytest
from datetime import date
from datetime_functions.get_days_in_month import get_days_in_month


def test_get_days_in_month_january() -> None:
    """
    Test case 1: Test get_days_in_month function with January.
    """
    result: int = get_days_in_month(2023, 1)
    assert isinstance(result, int)
    assert result == 31


def test_get_days_in_month_february_non_leap() -> None:
    """
    Test case 2: Test get_days_in_month function with February in non-leap year.
    """
    result: int = get_days_in_month(2023, 2)
    assert isinstance(result, int)
    assert result == 28


def test_get_days_in_month_february_leap() -> None:
    """
    Test case 3: Test get_days_in_month function with February in leap year.
    """
    result: int = get_days_in_month(2020, 2)
    assert isinstance(result, int)
    assert result == 29


def test_get_days_in_month_april() -> None:
    """
    Test case 4: Test get_days_in_month function with April.
    """
    result: int = get_days_in_month(2023, 4)
    assert isinstance(result, int)
    assert result == 30


def test_get_days_in_month_december() -> None:
    """
    Test case 5: Test get_days_in_month function with December.
    """
    result: int = get_days_in_month(2023, 12)
    assert isinstance(result, int)
    assert result == 31


def test_get_days_in_month_all_months() -> None:
    """
    Test case 6: Test get_days_in_month function for all months in non-leap year.
    """
    expected_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month, expected in enumerate(expected_days, 1):
        result: int = get_days_in_month(2023, month)
        assert result == expected


def test_get_days_in_month_all_months_leap() -> None:
    """
    Test case 7: Test get_days_in_month function for all months in leap year.
    """
    expected_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month, expected in enumerate(expected_days, 1):
        result: int = get_days_in_month(2020, month)
        assert result == expected


def test_get_days_in_month_from_date_object() -> None:
    """
    Test case 8: Test get_days_in_month function with date object.
    """
    test_date: date = date(2023, 6, 15)
    result: int = get_days_in_month(test_date)
    assert isinstance(result, int)
    assert result == 30  # June has 30 days


def test_get_days_in_month_invalid_month() -> None:
    """
    Test case 9: Test get_days_in_month function with invalid month raises ValueError.
    """
    with pytest.raises(ValueError):
        get_days_in_month(2023, 0)

    with pytest.raises(ValueError):
        get_days_in_month(2023, 13)

    with pytest.raises(ValueError):
        get_days_in_month(2023, -1)


def test_get_days_in_month_invalid_input_type() -> None:
    """
    Test case 10: Test get_days_in_month function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_days_in_month("2023", 1)

    with pytest.raises(TypeError):
        get_days_in_month(2023, "1")

    with pytest.raises(TypeError):
        get_days_in_month(None, 1)

    with pytest.raises(TypeError):
        get_days_in_month(2023, None)
