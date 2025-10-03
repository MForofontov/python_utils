import pytest
from network_functions.check_port_open import check_port_open
from unittest.mock import patch, MagicMock


def test_check_port_open_success() -> None:
    """
    Test case 1: Normal operation with valid host and open port.
    """
    with patch("socket.socket") as mock_socket:
        mock_instance = mock_socket.return_value
        mock_instance.connect.return_value = None
        assert check_port_open("localhost", 80) is True


def test_check_port_open_closed() -> None:
    """
    Test case 2: Port is closed, should return False.
    """
    with patch("socket.socket") as mock_socket:
        mock_instance = MagicMock()
        mock_instance.connect.side_effect = Exception()
        mock_socket.return_value.__enter__.return_value = mock_instance
        assert check_port_open("localhost", 81) is False


def test_check_port_open_type_error_host() -> None:
    """
    Test case 3: TypeError for non-string host.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        check_port_open(123, 80)


def test_check_port_open_type_error_port() -> None:
    """
    Test case 4: TypeError for non-integer port.
    """
    with pytest.raises(TypeError, match="port must be an integer"):
        check_port_open("localhost", "80")


def test_check_port_open_value_error_host() -> None:
    """
    Test case 5: ValueError for empty host.
    """
    with pytest.raises(ValueError, match="host cannot be empty"):
        check_port_open("", 80)


def test_check_port_open_value_error_port() -> None:
    """
    Test case 6: ValueError for out-of-range port.
    """
    with pytest.raises(ValueError, match="port must be between 1 and 65535"):
        check_port_open("localhost", 0)
    with pytest.raises(ValueError, match="port must be between 1 and 65535"):
        check_port_open("localhost", 70000)


def test_check_port_open_performance() -> None:
    """
    Test case 7: Performance with repeated calls.
    """
    with patch("socket.socket") as mock_socket:
        mock_instance = mock_socket.return_value
        mock_instance.connect.return_value = None
        for _ in range(100):
            assert check_port_open("localhost", 80) is True
