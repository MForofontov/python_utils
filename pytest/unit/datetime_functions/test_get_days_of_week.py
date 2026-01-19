import pytest

pytestmark = [pytest.mark.unit, pytest.mark.datetime]
from datetime_functions.get_days_of_week import get_days_of_week


def test_get_days_of_week_full_names() -> None:
    """
    Test case 1: Test get_days_of_week function returns full weekday names.
    """
    result: list[str] = get_days_of_week()
    assert isinstance(result, list)
    assert len(result) == 7
    assert result == [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def test_get_days_of_week_abbreviated_names() -> None:
    """
    Test case 2: Test get_days_of_week function returns abbreviated weekday names.
    """
    result: list[str] = get_days_of_week(short_names=True)
    assert isinstance(result, list)
    assert len(result) == 7
    assert result == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def test_get_days_of_week_all_strings() -> None:
    """
    Test case 3: Test get_days_of_week function returns all string elements.
    """
    result: list[str] = get_days_of_week()
    for day in result:
        assert isinstance(day, str)
        assert len(day) > 0


def test_get_days_of_week_abbreviated_all_strings() -> None:
    """
    Test case 4: Test get_days_of_week function returns all string elements when abbreviated.
    """
    result: list[str] = get_days_of_week(short_names=True)
    for day in result:
        assert isinstance(day, str)
        assert len(day) == 3  # Abbreviated days should be 3 characters


def test_get_days_of_week_invalid_abbreviated_type() -> None:
    """
    Test case 5: Test get_days_of_week function with invalid abbreviated type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_days_of_week(short_names="true")

    with pytest.raises(TypeError):
        get_days_of_week(short_names=1)

    with pytest.raises(TypeError):
        get_days_of_week(short_names=None)
