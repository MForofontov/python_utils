import pytest
from network_functions.get_dns_servers import get_dns_servers
from unittest.mock import mock_open, patch


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


def test_get_dns_servers_file_error() -> None:
    """
    Test case 3: File open error returns empty list.
    """
    with patch("builtins.open", side_effect=Exception()):
        servers = get_dns_servers()
        assert servers == []


def test_get_dns_servers_type() -> None:
    """
    Test case 4: Return type is always list.
    """
    servers = get_dns_servers()
    assert isinstance(servers, list)


def test_get_dns_servers_performance() -> None:
    """
    Test case 5: Performance with repeated calls.
    """
    m = mock_open(read_data="nameserver 8.8.8.8\n")
    with patch("builtins.open", m):
        for _ in range(50):
            servers = get_dns_servers()
            assert servers == ["8.8.8.8"]


def test_get_dns_servers_edge_case() -> None:
    """
    Test case 6: Edge case with unusual file content.
    """
    m = mock_open(read_data="nameserver not_an_ip\n")
    with patch("builtins.open", m):
        servers = get_dns_servers()
        assert servers == ["not_an_ip"]
