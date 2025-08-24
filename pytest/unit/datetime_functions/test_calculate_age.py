import pytest
from datetime import datetime, date
from datetime_functions.calculate_age import calculate_age


def test_calculate_age_basic() -> None:
    """
    Test calculate_age function with basic age calculation.
    """
    # Test case 1: Basic age calculation
    birth_date: date = date(1990, 1, 15)
    reference_date: date = date(2023, 1, 15)
    result: int = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_birthday_not_reached() -> None:
    """
    Test calculate_age function when birthday hasn't been reached this year.
    """
    # Test case 2: Birthday not reached this year
    birth_date: date = date(1990, 6, 15)
    reference_date: date = date(2023, 3, 15)
    result: int = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 32


def test_calculate_age_birthday_passed() -> None:
    """
    Test calculate_age function when birthday has passed this year.
    """
    # Test case 3: Birthday passed this year
    birth_date: date = date(1990, 3, 15)
    reference_date: date = date(2023, 6, 15)
    result: int = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_same_day() -> None:
    """
    Test calculate_age function when reference date is birth date.
    """
    # Test case 4: Same day (0 years old)
    birth_date: date = date(2023, 1, 15)
    reference_date: date = date(2023, 1, 15)
    result: int = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 0


def test_calculate_age_with_datetime_objects() -> None:
    """
    Test calculate_age function with datetime objects.
    """
    # Test case 5: Datetime objects
    birth_date: datetime = datetime(1990, 1, 15, 10, 30, 0)
    reference_date: datetime = datetime(2023, 1, 15, 15, 45, 0)
    result: int = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_mixed_types() -> None:
    """
    Test calculate_age function with mixed date and datetime objects.
    """
    # Test case 6: Mixed types
    birth_date: date = date(1990, 1, 15)
    reference_date: datetime = datetime(2023, 1, 15, 12, 0, 0)
    result: int = calculate_age(birth_date, reference_date)
    assert isinstance(result, int)
    assert result == 33


def test_calculate_age_default_reference() -> None:
    """
    Test calculate_age function with default reference date (today).
    """
    # Test case 7: Default reference date
    birth_date: date = date(2020, 1, 1)
    result: int = calculate_age(birth_date)
    assert isinstance(result, int)
    assert result >= 4  # Should be at least 4 years old as of 2025


def test_calculate_age_invalid_input_type() -> None:
    """
    Test calculate_age function with invalid input type raises TypeError.
    """
    # Test case 8: Invalid input types
    reference_date: date = date(2023, 1, 15)
    
    with pytest.raises(TypeError):
        calculate_age('1990-01-15', reference_date)
    
    with pytest.raises(TypeError):
        calculate_age(123, reference_date)
    
    with pytest.raises(TypeError):
        calculate_age(None, reference_date)


def test_calculate_age_future_birth_date() -> None:
    """
    Test calculate_age function with future birth date raises ValueError.
    """
    # Test case 9: Future birth date
    birth_date: date = date(2025, 1, 15)
    reference_date: date = date(2023, 1, 15)
    
    with pytest.raises(ValueError):
        calculate_age(birth_date, reference_date)
