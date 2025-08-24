import pytest
from datetime_functions.get_days_of_week import get_days_of_week


def test_get_days_of_week_full_names() -> None:
    """
    Test get_days_of_week function returns full weekday names.
    """
    # Test case 1: Full names
    result: list[str] = get_days_of_week()
    assert isinstance(result, list)
    assert len(result) == 7
    assert result == ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def test_get_days_of_week_abbreviated_names() -> None:
    """
    Test get_days_of_week function returns abbreviated weekday names.
    """
    # Test case 2: Abbreviated names
    result: list[str] = get_days_of_week(abbreviated=True)
    assert isinstance(result, list)
    assert len(result) == 7
    assert result == ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def test_get_days_of_week_all_strings() -> None:
    """
    Test get_days_of_week function returns all string elements.
    """
    # Test case 3: All elements are strings
    result: list[str] = get_days_of_week()
    for day in result:
        assert isinstance(day, str)
        assert len(day) > 0


def test_get_days_of_week_abbreviated_all_strings() -> None:
    """
    Test get_days_of_week function returns all string elements when abbreviated.
    """
    # Test case 4: All abbreviated elements are strings
    result: list[str] = get_days_of_week(abbreviated=True)
    for day in result:
        assert isinstance(day, str)
        assert len(day) == 3  # Abbreviated days should be 3 characters


def test_get_days_of_week_invalid_abbreviated_type() -> None:
    """
    Test get_days_of_week function with invalid abbreviated type raises TypeError.
    """
    # Test case 5: Invalid abbreviated parameter type
    with pytest.raises(TypeError):
        get_days_of_week(abbreviated='true')
    
    with pytest.raises(TypeError):
        get_days_of_week(abbreviated=1)
    
    with pytest.raises(TypeError):
        get_days_of_week(abbreviated=None)
