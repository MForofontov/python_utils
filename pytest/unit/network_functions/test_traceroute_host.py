import pytest
from network_functions.traceroute_host import traceroute_host
from unittest.mock import patch, MagicMock


def test_traceroute_host_normal() -> None:
    """
    Test case 1: Normal operation with mocked subprocess.
    """
    mock_result = MagicMock()
    mock_result.stdout = "1 192.168.1.1\n2 10.0.0.1\n"
    with patch("subprocess.run", return_value=mock_result):
        hops = traceroute_host("google.com", max_hops=2)
        assert hops == ["10.0.0.1"]


def test_traceroute_host_type_error_host() -> None:
    """
    Test case 2: TypeError for non-string host.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        traceroute_host(123)


def test_traceroute_host_value_error_empty() -> None:
    """
    Test case 3: ValueError for empty host.
    """
    with pytest.raises(ValueError, match="host cannot be empty"):
        traceroute_host("")


def test_traceroute_host_performance() -> None:
    """
    Test case 4: Performance with repeated calls.
    """
    mock_result = MagicMock()
    mock_result.stdout = "1 192.168.1.1\n2 10.0.0.1\n"
    with patch("subprocess.run", return_value=mock_result):
        for _ in range(5):
            hops = traceroute_host("google.com", max_hops=2)
            assert hops == ["10.0.0.1"]


def test_traceroute_host_error() -> None:
    """
    Test case 5: Exception in subprocess returns empty list.
    """
    with patch("subprocess.run", side_effect=Exception("fail")):
        hops = traceroute_host("google.com", max_hops=2)
        assert hops == []
