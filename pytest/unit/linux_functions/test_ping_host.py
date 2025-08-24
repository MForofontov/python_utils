import pytest
from linux_functions.ping_host import ping_host


def test_ping_localhost() -> None:
    """
    Test ping_host function with localhost returns True.
    """
    # Test case 1: Ping localhost (should be reachable)
    result: bool = ping_host('127.0.0.1')
    assert isinstance(result, bool)
    # localhost should generally be reachable
    assert result == True


def test_ping_invalid_host() -> None:
    """
    Test ping_host function with an invalid/unreachable host returns False.
    """
    # Test case 2: Use RFC5737 test address that should not be reachable
    result: bool = ping_host('192.0.2.1', timeout=1)
    assert isinstance(result, bool)
    # This should fail quickly
    assert result == False


def test_ping_with_custom_count() -> None:
    """
    Test ping_host function with custom count parameter.
    """
    # Test case 3: Ping with custom count
    result: bool = ping_host('127.0.0.1', count=2)
    assert isinstance(result, bool)


def test_ping_with_timeout() -> None:
    """
    Test ping_host function with custom timeout parameter.
    """
    # Test case 4: Ping with custom timeout
    result: bool = ping_host('127.0.0.1', timeout=1)
    assert isinstance(result, bool)


def test_ping_invalid_type() -> None:
    """
    Test ping_host function with invalid input type raises TypeError.
    """
    # Test case 5: Invalid input types
    with pytest.raises(TypeError):
        ping_host(123)
    
    with pytest.raises(TypeError):
        ping_host(None)
    
    with pytest.raises(TypeError):
        ping_host(['127.0.0.1'])
