from datetime import date, datetime
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.datetime]
from python_utils.datetime_functions.is_today import is_today


def test_is_today_with_today_date() -> None:
    """
    Test case 1: Test is_today function with today's date.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_date: date = date(2023, 6, 15)
        result: bool = is_today(test_date)
        assert isinstance(result, bool)
        assert result is True


def test_is_today_with_yesterday() -> None:
    """
    Test case 2: Test is_today function with yesterday's date.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_date: date = date(2023, 6, 14)
        result: bool = is_today(test_date)
        assert isinstance(result, bool)
        assert result is False


def test_is_today_with_tomorrow() -> None:
    """
    Test case 3: Test is_today function with tomorrow's date.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_date: date = date(2023, 6, 16)
        result: bool = is_today(test_date)
        assert isinstance(result, bool)
        assert result is False


def test_is_today_with_datetime() -> None:
    """
    Test case 4: Test is_today function with datetime object.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_datetime: datetime = datetime(2023, 6, 15, 14, 30, 45)
        result: bool = is_today(test_datetime)
        assert isinstance(result, bool)
        assert result is True


def test_is_today_with_datetime_different_day() -> None:
    """
    Test case 5: Test is_today function with datetime object for different day.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_datetime: datetime = datetime(2023, 6, 14, 23, 59, 59)
        result: bool = is_today(test_datetime)
        assert isinstance(result, bool)
        assert result is False


def test_is_today_with_different_year() -> None:
    """
    Test case 6: Test is_today function with different year.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_date: date = date(2022, 6, 15)
        result: bool = is_today(test_date)
        assert isinstance(result, bool)
        assert result is False


def test_is_today_with_different_month() -> None:
    """
    Test case 7: Test is_today function with different month.
    """
    with patch("datetime_functions.is_today.date") as mock_date:
        mock_date.today.return_value = date(2023, 6, 15)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        test_date: date = date(2023, 5, 15)
        result: bool = is_today(test_date)
        assert isinstance(result, bool)
        assert result is False


def test_is_today_invalid_input_type() -> None:
    """
    Test case 8: Test is_today function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        is_today("2023-06-15")

    with pytest.raises(TypeError):
        is_today(123)

    with pytest.raises(TypeError):
        is_today(None)
