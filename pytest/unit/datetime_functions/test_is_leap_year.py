import pytest

try:
    import pytz
    from pyutils_collection.datetime_functions.is_leap_year import is_leap_year
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False
    pytz = None  # type: ignore
    is_leap_year = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.datetime,
    pytest.mark.skipif(not PYTZ_AVAILABLE, reason="pytz not installed"),
]


def test_is_leap_year_true_cases() -> None:
    """
    Test case 1: Test is_leap_year function with years that are leap years.
    """
    assert is_leap_year(2000)  # Divisible by 400
    assert is_leap_year(2004)  # Divisible by 4, not by 100
    assert is_leap_year(2020)  # Divisible by 4, not by 100
    assert is_leap_year(1600)  # Divisible by 400


def test_is_leap_year_false_cases() -> None:
    """
    Test case 2: Test is_leap_year function with years that are not leap years.
    """
    assert not is_leap_year(1900)  # Divisible by 100, not by 400
    assert not is_leap_year(2001)  # Not divisible by 4
    assert not is_leap_year(2003)  # Not divisible by 4
    assert not is_leap_year(1700)  # Divisible by 100, not by 400


def test_is_leap_year_edge_cases() -> None:
    """
    Test case 3: Test is_leap_year function with edge cases.
    """
    assert not is_leap_year(1)  # Year 1
    assert is_leap_year(4)  # Year 4
    assert not is_leap_year(100)  # Year 100
    assert is_leap_year(400)  # Year 400


def test_is_leap_year_negative_years() -> None:
    """
    Test case 4: Test is_leap_year function with negative years.
    """
    assert is_leap_year(-4)  # 4 BCE
    assert not is_leap_year(-1)  # 1 BCE
    assert not is_leap_year(-100)  # 100 BCE
    assert is_leap_year(-400)  # 400 BCE


def test_is_leap_year_invalid_input_type() -> None:
    """
    Test case 5: Test is_leap_year function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        is_leap_year("2020")

    with pytest.raises(TypeError):
        is_leap_year(2020.0)

    with pytest.raises(TypeError):
        is_leap_year(None)

    with pytest.raises(TypeError):
        is_leap_year([2020])
