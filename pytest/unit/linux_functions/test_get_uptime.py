import pytest
from linux_functions.get_uptime import get_uptime


def test_get_uptime_returns_positive_float() -> None:
    """
    Test case 1: Test the get_uptime function returns a positive float value.
    """
    uptime: float = get_uptime()
    
    # Uptime should be a positive number
    assert isinstance(uptime, float)
    assert uptime > 0
    
    # Uptime should be reasonable (less than 1 year in seconds)
    assert uptime < 365 * 24 * 3600
