"""Tests for local SSH check connection using subprocess."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

try:
    import paramiko
    from python_utils.ssh_functions.local.ssh_check_connection import ssh_check_connection
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    paramiko = None  # type: ignore
    ssh_check_connection = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.ssh_functions,
    pytest.mark.skipif(not PARAMIKO_AVAILABLE, reason="paramiko not installed"),
]


def test_ssh_check_connection_successful() -> None:
    """
    Test case 1: Successful connection check.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_check_connection("host", user="user")
        assert result["success"] is True
        assert result["exit_code"] == 0


def test_ssh_check_connection_failed() -> None:
    """
    Test case 2: Failed connection check.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="error", returncode=1)
        result = ssh_check_connection("host", user="user")
        assert result["success"] is False
        assert result["exit_code"] == 1


def test_ssh_check_connection_with_custom_port() -> None:
    """
    Test case 3: Connection check with custom port.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_check_connection("host", user="user", port=2222)
        assert result["success"] is True


def test_ssh_check_connection_without_user() -> None:
    """
    Test case 4: Connection check without specifying user.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_check_connection("host")
        assert result["success"] is True


def test_ssh_check_connection_boundary_port_min() -> None:
    """
    Test case 5: Connection check with minimum port value.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_check_connection("host", port=1)
        assert result["success"] is True


def test_ssh_check_connection_boundary_port_max() -> None:
    """
    Test case 6: Connection check with maximum port value.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_check_connection("host", port=65535)
        assert result["success"] is True


def test_ssh_check_connection_type_error_host() -> None:
    """
    Test case 7: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_check_connection(123)


def test_ssh_check_connection_type_error_user() -> None:
    """
    Test case 8: TypeError for invalid user type.
    """
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_check_connection("host", user=123)


def test_ssh_check_connection_type_error_port() -> None:
    """
    Test case 9: TypeError for invalid port type.
    """
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_check_connection("host", port="22")


def test_ssh_check_connection_type_error_timeout() -> None:
    """
    Test case 10: TypeError for invalid timeout type.
    """
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_check_connection("host", timeout="10")


def test_ssh_check_connection_value_error_port_too_low() -> None:
    """
    Test case 11: ValueError for port value too low.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_check_connection("host", port=0)


def test_ssh_check_connection_value_error_port_too_high() -> None:
    """
    Test case 12: ValueError for port value too high.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_check_connection("host", port=70000)


def test_ssh_check_connection_value_error_timeout_negative() -> None:
    """
    Test case 13: ValueError for negative timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_check_connection("host", timeout=-5)


def test_ssh_check_connection_value_error_timeout_zero() -> None:
    """
    Test case 14: ValueError for zero timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_check_connection("host", timeout=0)


def test_ssh_check_connection_runtime_error_timeout() -> None:
    """
    Test case 15: RuntimeError when connection times out.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired("ssh", 10)
        with pytest.raises(RuntimeError, match="SSH connection timed out"):
            ssh_check_connection("host")


def test_ssh_check_connection_runtime_error_general() -> None:
    """
    Test case 16: RuntimeError for general subprocess failure.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("Connection failed")
        with pytest.raises(RuntimeError, match="SSH connection failed"):
            ssh_check_connection("host")
