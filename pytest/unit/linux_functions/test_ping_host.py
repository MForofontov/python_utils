import pytest
from linux_functions.ping_host import ping_host


def test_ping_localhost() -> None:
    """
    Test case 1: Test ping_host function with localhost returns True.
    """
    result: bool = ping_host("127.0.0.1")
    assert isinstance(result, bool)
    # localhost should generally be reachable
    assert result


def test_ping_invalid_host() -> None:
    """
    Test case 2: Test ping_host function with an invalid/unreachable host returns False.
    """
    result: bool = ping_host("192.0.2.1", timeout=1)
    assert isinstance(result, bool)
    # This should fail quickly
    assert not result


def test_ping_with_custom_count() -> None:
    """
    Test case 3: Test ping_host function with custom count parameter.
    """
    result: bool = ping_host("127.0.0.1", count=2)
    assert isinstance(result, bool)


def test_ping_with_timeout() -> None:
    """
    Test case 4: Test ping_host function with custom timeout parameter.
    """
    result: bool = ping_host("127.0.0.1", timeout=1)
    assert isinstance(result, bool)


def test_ping_invalid_type() -> None:
    """
    Test case 5: Test ping_host function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        ping_host(123)

    with pytest.raises(TypeError):
        ping_host(None)

    with pytest.raises(TypeError):
        ping_host(["127.0.0.1"])
