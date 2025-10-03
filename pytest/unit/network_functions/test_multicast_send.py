import pytest
from network_functions.multicast_send import multicast_send
from unittest.mock import patch, MagicMock
import socket



def test_multicast_send_normal() -> None:
    """
    Test case 1: Normal operation with mocked socket.
    """
    mock_sock = MagicMock()
    with patch("socket.socket", return_value=mock_sock):
        with patch.object(mock_sock, "setsockopt"):
            with patch.object(mock_sock, "sendto"):
                with patch.object(mock_sock, "close"):
                    multicast_send("hello", "224.0.0.1", 5007)
                    mock_sock.sendto.assert_called_once()

def test_multicast_send_type_error_message() -> None:
    """
    Test case 2: TypeError for non-string message (simulate error).
    """
    with pytest.raises(Exception):
        multicast_send(123, "224.0.0.1", 5007)

def test_multicast_send_type_error_group() -> None:
    """
    Test case 3: TypeError for non-string group (simulate error).
    """
    with pytest.raises(Exception):
        multicast_send("hello", 123, 5007)

def test_multicast_send_type_error_port() -> None:
    """
    Test case 4: TypeError for non-integer port (simulate error).
    """
    with pytest.raises(Exception):
        multicast_send("hello", "224.0.0.1", "not_an_int")
