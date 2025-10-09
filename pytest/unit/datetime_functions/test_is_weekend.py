from datetime import datetime
import pytest
from datetime_functions.is_weekend import is_weekend

def test_is_weekend_monday() -> None:
    """
    Test case 1: is_weekend returns False for a Monday datetime.
    """
    test_datetime = datetime(2023, 6, 5, 10, 0, 0)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False

def test_is_weekend_tuesday() -> None:
    """
    Test case 2: is_weekend returns False for a Tuesday datetime.
    """
    test_datetime = datetime(2023, 6, 6, 8, 0, 0)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False

def test_is_weekend_wednesday() -> None:
    """
    Test case 3: is_weekend returns False for a Wednesday datetime.
    """
    test_datetime = datetime(2023, 6, 7, 12, 0, 0)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False

def test_is_weekend_thursday() -> None:
    """
    Test case 4: is_weekend returns False for a Thursday datetime.
    """
    test_datetime = datetime(2023, 6, 8, 18, 0, 0)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False



def test_is_weekend_friday() -> None:
    """
    Test case 5: is_weekend returns False for a Friday datetime.
    """
    test_datetime = datetime(2023, 6, 9, 23, 0, 0)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is False

def test_is_weekend_saturday() -> None:
    """
    Test case 6: is_weekend returns True for a Saturday datetime.
    """
    test_datetime = datetime(2023, 6, 10, 14, 0, 0)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is True

def test_is_weekend_sunday() -> None:
    """
    Test case 7: is_weekend returns True for a Sunday datetime.
    """
    test_datetime = datetime(2023, 6, 11, 23, 59, 59)
    result = is_weekend(test_datetime)
    assert isinstance(result, bool)
    assert result is True

def test_is_weekend_invalid_type() -> None:
    """
    Test case 8: is_weekend raises TypeError for invalid input types.
    """
    with pytest.raises(TypeError):
        is_weekend("2023-06-10")
    with pytest.raises(TypeError):
        is_weekend(123)
    with pytest.raises(TypeError):
        is_weekend(None)
