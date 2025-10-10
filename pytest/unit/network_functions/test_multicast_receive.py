from unittest.mock import MagicMock, patch

import pytest
from network_functions.multicast_receive import multicast_receive


def test_multicast_receive_normal() -> None:
    """
    Test case 1: Normal operation with mocked socket.
    """
    mock_sock = MagicMock()
    mock_sock.recvfrom.return_value = (b"hello", None)
    with patch("socket.socket", return_value=mock_sock):
        with patch.object(mock_sock, "settimeout"):
            with patch.object(mock_sock, "setsockopt"):
                with patch.object(mock_sock, "bind"):
                    with patch.object(mock_sock, "close"):
                        result = multicast_receive("224.0.0.1", 5007, timeout=1)
                        assert result == "hello"


def test_multicast_receive_timeout() -> None:
    """
    Test case 2: Timeout returns None.
    """
    mock_sock = MagicMock()
    mock_sock.recvfrom.side_effect = TimeoutError()
    with patch("socket.socket", return_value=mock_sock):
        with patch.object(mock_sock, "settimeout"):
            with patch.object(mock_sock, "setsockopt"):
                with patch.object(mock_sock, "bind"):
                    with patch.object(mock_sock, "close"):
                        result = multicast_receive("224.0.0.1", 5007, timeout=1)
                        assert result is None


def test_multicast_receive_type_error_group() -> None:
    """
    Test case 3: TypeError for non-string group (simulate error).
    """
    with pytest.raises(Exception):
        multicast_receive(123, 5007)


def test_multicast_receive_type_error_port() -> None:
    """
    Test case 4: TypeError for non-integer port (simulate error).
    """
    with pytest.raises(Exception):
        multicast_receive("224.0.0.1", "not_an_int")
