import socket
from unittest.mock import patch

import pytest
from network_functions.get_subnet_mask import get_subnet_mask


def test_get_subnet_mask_normal() -> None:
    """
    Test case 1: Normal operation with mocked interface.
    """

    class Addr:
        def __init__(self, netmask: str) -> None:
            self.family = socket.AF_INET
            self.netmask = netmask

    with patch("psutil.net_if_addrs", return_value={"eth0": [Addr("255.255.255.0")]}):
        mask = get_subnet_mask("eth0")
        assert mask == "255.255.255.0"


def test_get_subnet_mask_not_found() -> None:
    """
    Test case 2: Interface not found returns empty string.
    """
    with patch("psutil.net_if_addrs", return_value={}):
        mask = get_subnet_mask("eth0")
        assert mask == ""


def test_get_subnet_mask_no_inet() -> None:
    """
    Test case 3: No AF_INET address returns empty string.
    """

    class Addr:
        def __init__(self) -> None:
            self.family = socket.AF_INET + 1
            self.netmask = None

    with patch("psutil.net_if_addrs", return_value={"eth0": [Addr()]}):
        mask = get_subnet_mask("eth0")
        assert mask == ""


def test_get_subnet_mask_type_error() -> None:
    """
    Test case 4: TypeError for non-string interface (simulate error).
    """
    with pytest.raises(TypeError, match="interface must be a string"):
        get_subnet_mask(123)


def test_get_subnet_mask_value_error_empty() -> None:
    """Test case 5: ValueError for empty interface string."""
    with pytest.raises(ValueError, match="interface cannot be empty"):
        get_subnet_mask("")
