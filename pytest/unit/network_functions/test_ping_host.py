import pytest
from network_functions.ping_host import ping_host
from unittest.mock import patch, MagicMock


def test_ping_host_success() -> None:
    """
    Test case 1: Host is reachable (mocked subprocess).
    """
    mock_result = MagicMock()
    mock_result.returncode = 0
    with patch("subprocess.run", return_value=mock_result):
        assert ping_host("8.8.8.8") is True


def test_ping_host_unreachable() -> None:
    """
    Test case 2: Host is unreachable (mocked subprocess).
    """
    mock_result = MagicMock()
    mock_result.returncode = 1
    with patch("subprocess.run", return_value=mock_result):
        assert ping_host("8.8.8.8") is False


def test_ping_host_type_error_host() -> None:
    """
    Test case 3: TypeError for non-string host.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ping_host(123)


def test_ping_host_value_error_host() -> None:
    """
    Test case 4: ValueError for empty host.
    """
    with pytest.raises(ValueError, match="host cannot be empty"):
        ping_host("")


def test_ping_host_type_error_count() -> None:
    """
    Test case 5: TypeError for non-integer count.
    """
    with pytest.raises(TypeError, match="count must be an integer"):
        ping_host("8.8.8.8", count="not_an_int")


def test_ping_host_type_error_timeout() -> None:
    """
    Test case 6: TypeError for non-integer timeout.
    """
    with pytest.raises(TypeError, match="timeout must be an integer"):
        ping_host("8.8.8.8", timeout="not_an_int")


def test_ping_host_performance() -> None:
    """
    Test case 7: Performance with repeated calls.
    """
    mock_result = MagicMock()
    mock_result.returncode = 0
    with patch("subprocess.run", return_value=mock_result):
        for _ in range(10):
            assert ping_host("8.8.8.8") is True
