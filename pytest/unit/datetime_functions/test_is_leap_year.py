import pytest
from datetime_functions.is_leap_year import is_leap_year


def test_is_leap_year_true_cases() -> None:
    """
    Test case 1: Test is_leap_year function with years that are leap years.
    """
    assert is_leap_year(2000) == True  # Divisible by 400
    assert is_leap_year(2004) == True  # Divisible by 4, not by 100
    assert is_leap_year(2020) == True  # Divisible by 4, not by 100
    assert is_leap_year(1600) == True  # Divisible by 400


def test_is_leap_year_false_cases() -> None:
    """
    Test case 2: Test is_leap_year function with years that are not leap years.
    """
    assert is_leap_year(1900) == False  # Divisible by 100, not by 400
    assert is_leap_year(2001) == False  # Not divisible by 4
    assert is_leap_year(2003) == False  # Not divisible by 4
    assert is_leap_year(1700) == False  # Divisible by 100, not by 400


def test_is_leap_year_edge_cases() -> None:
    """
    Test case 3: Test is_leap_year function with edge cases.
    """
    assert is_leap_year(1) == False    # Year 1
    assert is_leap_year(4) == True     # Year 4
    assert is_leap_year(100) == False  # Year 100
    assert is_leap_year(400) == True   # Year 400


def test_is_leap_year_negative_years() -> None:
    """
    Test case 4: Test is_leap_year function with negative years.
    """
    assert is_leap_year(-4) == True    # 4 BCE
    assert is_leap_year(-1) == False   # 1 BCE
    assert is_leap_year(-100) == False # 100 BCE
    assert is_leap_year(-400) == True  # 400 BCE


def test_is_leap_year_invalid_input_type() -> None:
    """
    Test case 5: Test is_leap_year function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        is_leap_year('2020')
    
    with pytest.raises(TypeError):
        is_leap_year(2020.0)
    
    with pytest.raises(TypeError):
        is_leap_year(None)
    
    with pytest.raises(TypeError):
        is_leap_year([2020])
