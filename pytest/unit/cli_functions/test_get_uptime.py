import pytest

pytestmark = [pytest.mark.unit, pytest.mark.cli_functions]
from cli_functions.get_uptime import get_uptime


def test_get_uptime_returns_positive_float() -> None:
    """
    Test case 1: Test the get_uptime function returns a positive float value.
    """
    uptime = get_uptime()

    # Uptime should be a positive number
    assert isinstance(uptime, float)
    assert uptime > 0


def test_get_uptime_reasonable_value() -> None:
    """
    Test case 2: Verify uptime is within reasonable bounds.
    """
    uptime = get_uptime()

    # Uptime should be less than 1 year in seconds (reasonable for most systems)
    assert uptime < 365 * 24 * 3600
    # Uptime should be at least a few seconds
    assert uptime > 0.001


def test_get_uptime_consistency() -> None:
    """
    Test case 3: Verify uptime increases over time.
    """
    import time

    uptime1 = get_uptime()
    time.sleep(0.1)
    uptime2 = get_uptime()

    # Second measurement should be larger
    assert uptime2 > uptime1
    # Difference should be approximately the sleep duration
    assert 0.05 < (uptime2 - uptime1) < 0.5


def test_get_uptime_return_type() -> None:
    """
    Test case 4: Verify return type is consistently float.
    """
    uptime = get_uptime()
    assert type(uptime) is float


def test_get_uptime_multiple_calls() -> None:
    """
    Test case 5: Verify multiple calls work correctly.
    """
    uptimes = [get_uptime() for _ in range(5)]

    # All should be positive
    for uptime in uptimes:
        assert uptime > 0
        assert isinstance(uptime, float)


def test_get_uptime_monotonic_increase() -> None:
    """
    Test case 6: Verify uptime is monotonically increasing.
    """
    import time

    previous = get_uptime()
    for _ in range(3):
        time.sleep(0.05)
        current = get_uptime()
        assert current > previous
        previous = current
