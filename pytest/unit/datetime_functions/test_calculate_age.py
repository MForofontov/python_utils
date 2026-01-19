from datetime import datetime

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.datetime]
from python_utils.datetime_functions.calculate_age import calculate_age


def test_calculate_age_basic() -> None:
    """
    Test case 1: calculate_age returns correct age for typical input.
    """
    birth_date = datetime(1990, 1, 15, 0, 0, 0)
    reference_date = datetime(2023, 1, 15, 0, 0, 0)
    result = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_birthday_not_reached() -> None:
    """
    Test case 2: calculate_age returns correct age when birthday not reached this year.
    """
    birth_date = datetime(1990, 6, 15, 0, 0, 0)
    reference_date = datetime(2023, 3, 15, 0, 0, 0)
    result = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 32


def test_calculate_age_birthday_passed() -> None:
    """
    Test case 3: calculate_age returns correct age when birthday has passed this year.
    """
    birth_date = datetime(1990, 3, 15, 0, 0, 0)
    reference_date = datetime(2023, 6, 15, 0, 0, 0)
    result = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_same_day() -> None:
    """
    Test case 4: calculate_age returns 0 when reference date is birth date.
    """
    birth_date = datetime(2023, 1, 15, 0, 0, 0)
    reference_date = datetime(2023, 1, 15, 0, 0, 0)
    result = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 0


def test_calculate_age_with_datetime_objects() -> None:
    """
    Test case 5: calculate_age works with datetime objects with time.
    """
    birth_date = datetime(1990, 1, 15, 10, 30, 0)
    reference_date = datetime(2023, 1, 15, 15, 45, 0)
    result = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_default_reference() -> None:
    """
    Test case 6: calculate_age uses current date as default reference.
    """
    birth_date = datetime(2020, 1, 1, 0, 0, 0)
    result = calculate_age(birth_date)
    assert isinstance(result, int)
    assert result >= 4  # Should be at least 4 years old as of 2025

    # Removed: covered by test_calculate_age_type_error_on_non_datetime


def test_calculate_age_type_error_on_non_datetime() -> None:
    """
    Test case 7: calculate_age raises TypeError if birth_date is not datetime.
    """
    reference_date = datetime(2023, 1, 15, 12, 0, 0)
    with pytest.raises(TypeError):
        calculate_age("1990-01-15", reference_date)
    with pytest.raises(TypeError):
        calculate_age(123, reference_date)
    with pytest.raises(TypeError):
        calculate_age(None, reference_date)


def test_calculate_age_type_error_reference_date() -> None:
    """
    Test case 8: calculate_age raises TypeError if reference_date is not datetime.
    """
    birth_date = datetime(1990, 1, 15, 0, 0, 0)
    with pytest.raises(TypeError, match="reference_date must be a datetime object"):
        calculate_age(birth_date, "2023-01-15")  # type: ignore


def test_calculate_age_future_birth_date() -> None:
    """
    Test case 9: calculate_age raises ValueError if birth date is in the future.
    """
    birth_date = datetime(2025, 1, 15, 0, 0, 0)
    reference_date = datetime(2023, 1, 15, 0, 0, 0)
    with pytest.raises(ValueError, match="birth_date cannot be in the future"):
        calculate_age(birth_date, reference_date)
