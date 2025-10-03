import pytest
from network_functions.get_public_ip import get_public_ip
from unittest.mock import patch



def test_get_public_ip_type() -> None:
    """
    Test case 1: get_public_ip returns a string.
    """
    ip = get_public_ip()
    assert isinstance(ip, str)

def test_get_public_ip_format() -> None:
    """
    Test case 2: IP address format is correct (IPv4).
    """
    ip = get_public_ip()
    parts = ip.split(".")
    assert len(parts) == 4
    assert all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

def test_get_public_ip_mocked() -> None:
    """
    Test case 3: Mock requests.get returns expected IP.
    """
    class MockResponse:
        def __init__(self, text: str) -> None:
            self.text = text
        def raise_for_status(self) -> None:
            pass
    with patch("requests.get", return_value=MockResponse("8.8.8.8")):
        ip = get_public_ip()
        assert ip == "8.8.8.8"

def test_get_public_ip_network_error() -> None:
    """
    Test case 4: Network error raises exception.
    """
    class MockResponse:
        def raise_for_status(self) -> None:
            raise Exception("Network error")
        @property
        def text(self) -> str:
            return ""
    with patch("requests.get", return_value=MockResponse()):
        ip = get_public_ip()
        assert ip == ""

def test_get_public_ip_type_error() -> None:
    """
    Test case 5: TypeError if requests.get returns wrong type.
    """
    with patch("requests.get", return_value="not_a_response"):
        ip = get_public_ip()
        assert ip == ""
