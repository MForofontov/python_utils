"""Tests for remote SSH check connection using paramiko."""

from unittest.mock import MagicMock, patch

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    paramiko = None  # type: ignore

import pytest
from ssh_functions.remote.ssh_check_connection import ssh_check_connection

pytestmark = pytest.mark.skipif(not PARAMIKO_AVAILABLE, reason="paramiko not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.ssh_functions]


def test_ssh_check_connection_successful_with_password() -> None:
    """
    Test case 1: Successful connection check with password authentication.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection("host", user="user", password="pass")
            assert result["success"] is True
            assert result["message"] == "Connection successful"
            assert result["error"] is None


def test_ssh_check_connection_successful_with_key_file() -> None:
    """
    Test case 2: Successful connection check with key file authentication.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection(
                "host", user="user", key_filename="/path/to/key"
            )
            assert result["success"] is True
            assert result["message"] == "Connection successful"


def test_ssh_check_connection_with_custom_port() -> None:
    """
    Test case 3: Connection check with custom port.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection(
                "host", user="user", password="pass", port=2222
            )
            assert result["success"] is True
            mock_ssh.connect.assert_called_once_with(
                hostname="host",
                port=2222,
                username="user",
                password="pass",
                key_filename=None,
                timeout=10.0,
            )


def test_ssh_check_connection_default_user() -> None:
    """
    Test case 4: Connection check with default user from getpass.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="currentuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection("host", password="pass")
            assert result["success"] is True
            mock_ssh.connect.assert_called_once_with(
                hostname="host",
                port=22,
                username="currentuser",
                password="pass",
                key_filename=None,
                timeout=10.0,
            )


def test_ssh_check_connection_with_custom_timeout() -> None:
    """
    Test case 5: Connection check with custom timeout.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection(
                "host", user="user", password="pass", timeout=30.0
            )
            assert result["success"] is True
            mock_ssh.connect.assert_called_once_with(
                hostname="host",
                port=22,
                username="user",
                password="pass",
                key_filename=None,
                timeout=30.0,
            )


def test_ssh_check_connection_boundary_port_min() -> None:
    """
    Test case 6: Connection check with minimum port value.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection("host", user="user", password="pass", port=1)
            assert result["success"] is True


def test_ssh_check_connection_boundary_port_max() -> None:
    """
    Test case 7: Connection check with maximum port value.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh

            result = ssh_check_connection(
                "host", user="user", password="pass", port=65535
            )
            assert result["success"] is True


def test_ssh_check_connection_type_error_host() -> None:
    """
    Test case 8: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_check_connection(123)


def test_ssh_check_connection_type_error_user() -> None:
    """
    Test case 9: TypeError for invalid user type.
    """
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_check_connection("host", user=123)


def test_ssh_check_connection_type_error_password() -> None:
    """
    Test case 10: TypeError for invalid password type.
    """
    with pytest.raises(TypeError, match="password must be a string or None"):
        ssh_check_connection("host", password=123)


def test_ssh_check_connection_type_error_key_filename() -> None:
    """
    Test case 11: TypeError for invalid key_filename type.
    """
    with pytest.raises(TypeError, match="key_filename must be a string or None"):
        ssh_check_connection("host", key_filename=123)


def test_ssh_check_connection_type_error_port() -> None:
    """
    Test case 12: TypeError for invalid port type.
    """
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_check_connection("host", port="22")


def test_ssh_check_connection_type_error_timeout() -> None:
    """
    Test case 13: TypeError for invalid timeout type.
    """
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_check_connection("host", timeout="10")


def test_ssh_check_connection_value_error_port_too_low() -> None:
    """
    Test case 14: ValueError for port value too low.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_check_connection("host", port=0)


def test_ssh_check_connection_value_error_port_too_high() -> None:
    """
    Test case 15: ValueError for port value too high.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_check_connection("host", port=70000)


def test_ssh_check_connection_value_error_timeout_negative() -> None:
    """
    Test case 16: ValueError for negative timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_check_connection("host", timeout=-5)


def test_ssh_check_connection_value_error_timeout_zero() -> None:
    """
    Test case 17: ValueError for zero timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_check_connection("host", timeout=0)


def test_ssh_check_connection_auth_failure() -> None:
    """
    Test case 18: Authentication failure returns failure status.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh
            import paramiko

            mock_ssh.connect.side_effect = paramiko.AuthenticationException(
                "Auth failed"
            )

            result = ssh_check_connection("host", user="user", password="badpass")
            assert result["success"] is False
            assert result["message"] == "Authentication failed"
            assert "Auth failed" in result["error"]


def test_ssh_check_connection_ssh_exception() -> None:
    """
    Test case 19: SSH exception returns failure status.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh
            import paramiko

            mock_ssh.connect.side_effect = paramiko.SSHException("SSH error")

            result = ssh_check_connection("host", user="user", password="pass")
            assert result["success"] is False
            assert result["message"] == "SSH connection error"


def test_ssh_check_connection_timeout() -> None:
    """
    Test case 20: Timeout returns failure status.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh
            mock_ssh.connect.side_effect = TimeoutError("Connection timed out")

            result = ssh_check_connection(
                "host", user="user", password="pass", timeout=5.0
            )
            assert result["success"] is False
            assert "timed out after 5.0 seconds" in result["message"]


def test_ssh_check_connection_general_failure() -> None:
    """
    Test case 21: General exception returns failure status.
    """
    with patch(
        "ssh_functions.remote.ssh_check_connection.paramiko.SSHClient"
    ) as mock_client:
        with patch(
            "ssh_functions.remote.ssh_check_connection.getpass.getuser",
            return_value="testuser",
        ):
            mock_ssh = MagicMock()
            mock_client.return_value = mock_ssh
            mock_ssh.connect.side_effect = Exception("Connection refused")

            result = ssh_check_connection("host", user="user", password="pass")
            assert result["success"] is False
            assert result["message"] == "Connection failed"
            assert "Connection refused" in result["error"]
