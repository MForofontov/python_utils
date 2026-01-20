import pytest

try:
    from unittest.mock import mock_open, patch
    from pyutils_collection.network_functions.get_dns_servers import get_dns_servers
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    mock_open = None  # type: ignore
    patch = None  # type: ignore
    get_dns_servers = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.network_functions,
    pytest.mark.skipif(not PSUTIL_AVAILABLE, reason="psutil not installed"),
]


def test_get_dns_servers_normal() -> None:
    """
    Test case 1: Normal operation returns a list of IPs.
    """
    m = mock_open(read_data="nameserver 8.8.8.8\nnameserver 1.1.1.1\n")
    with patch("builtins.open", m):
        servers = get_dns_servers()
        assert servers == ["8.8.8.8", "1.1.1.1"]


def test_get_dns_servers_empty() -> None:
    """
    Test case 2: No nameserver lines returns empty list.
    """
    m = mock_open(read_data="search localdomain\n")
    with patch("builtins.open", m):
        servers = get_dns_servers()
        assert servers == []


def test_get_dns_servers_type() -> None:
    """
    Test case 3: Return type is always list.
    """
    servers = get_dns_servers()
    assert isinstance(servers, list)


def test_get_dns_servers_edge_case() -> None:
    """
    Test case 4: Edge case with unusual file content.
    """
    m = mock_open(read_data="nameserver not_an_ip\n")
    with patch("builtins.open", m):
        servers = get_dns_servers()
        assert servers == ["not_an_ip"]


def test_get_dns_servers_file_error() -> None:
    """
    Test case 5: File open error returns empty list.
    """
    with patch("builtins.open", side_effect=Exception()):
        servers = get_dns_servers()
        assert servers == []
