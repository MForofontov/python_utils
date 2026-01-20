from unittest.mock import MagicMock, patch

try:
    import psutil
    from python_utils.network_functions.is_port_listening import is_port_listening

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None  # type: ignore
    is_port_listening = None  # type: ignore

import pytest

pytestmark = pytest.mark.skipif(not PSUTIL_AVAILABLE, reason="psutil not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.network_functions]


def test_is_port_listening_true() -> None:
    """
    Test case 1: Port is being listened to (mocked).
    """
    mock_conn = MagicMock()
    mock_conn.laddr.port = 8080
    mock_conn.status = "LISTEN"
    with patch("psutil.net_connections", return_value=[mock_conn]):
        assert is_port_listening(8080) is True


def test_is_port_listening_false() -> None:
    """
    Test case 2: Port is not being listened to.
    """
    mock_conn = MagicMock()
    mock_conn.laddr.port = 8081
    mock_conn.status = "CLOSE"
    with patch("psutil.net_connections", return_value=[mock_conn]):
        assert is_port_listening(8080) is False


def test_is_port_listening_empty() -> None:
    """
    Test case 3: No connections returns False.
    """
    with patch("psutil.net_connections", return_value=[]):
        assert is_port_listening(8080) is False


def test_is_port_listening_type_error() -> None:
    """
    Test case 4: TypeError for non-integer port (simulate error).
    """
    with pytest.raises((TypeError, AttributeError, psutil.AccessDenied)):
        is_port_listening("not_an_int")
