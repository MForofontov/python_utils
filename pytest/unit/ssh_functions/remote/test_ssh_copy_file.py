"""Tests for remote SSH copy file using paramiko."""

from unittest.mock import MagicMock, patch

try:
    import paramiko  # noqa: F401

    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

import pytest
from ssh_functions.remote.ssh_copy_file import ssh_copy_file

pytestmark = pytest.mark.skipif(not PARAMIKO_AVAILABLE, reason="paramiko not installed")
pytestmark = [pytestmark, pytest.mark.unit, pytest.mark.ssh_functions]


def test_ssh_copy_file_successful_with_password() -> None:
    """
    Test case 1: Test successful file copy with password authentication.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=1024,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                        )
                        assert result["success"] is True
                        assert result["message"] == "File transferred successfully"
                        assert result["bytes_transferred"] == 1024
                        mock_sftp.put.assert_called_once_with(
                            "local.txt", "/remote/path.txt"
                        )


def test_ssh_copy_file_successful_with_key_file() -> None:
    """
    Test case 2: Test successful file copy with key file authentication.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=2048,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            key_filename="/path/to/key",
                        )
                        assert result["success"] is True
                        assert result["bytes_transferred"] == 2048


def test_ssh_copy_file_with_custom_port() -> None:
    """
    Test case 3: Test file copy with custom port.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=512,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                            port=2222,
                        )
                        assert result["success"] is True
                        mock_ssh.connect.assert_called_once_with(
                            hostname="host",
                            port=2222,
                            username="user",
                            password="pass",
                            key_filename=None,
                            timeout=30.0,
                        )


def test_ssh_copy_file_default_user() -> None:
    """
    Test case 4: Test file copy with default user from getpass.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="currentuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=256,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt", "/remote/path.txt", "host", password="pass"
                        )
                        assert result["success"] is True
                        mock_ssh.connect.assert_called_once_with(
                            hostname="host",
                            port=22,
                            username="currentuser",
                            password="pass",
                            key_filename=None,
                            timeout=30.0,
                        )


def test_ssh_copy_file_with_custom_timeout() -> None:
    """
    Test case 5: Test file copy with custom timeout.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=4096,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                            timeout=60.0,
                        )
                        assert result["success"] is True


def test_ssh_copy_file_boundary_port_min() -> None:
    """
    Test case 6: Test file copy with minimum port value.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=128,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                            port=1,
                        )
                        assert result["success"] is True


def test_ssh_copy_file_boundary_port_max() -> None:
    """
    Test case 7: Test file copy with maximum port value.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    with patch(
                        "ssh_functions.remote.ssh_copy_file.os.path.getsize",
                        return_value=128,
                    ):
                        mock_ssh = MagicMock()
                        mock_client.return_value = mock_ssh
                        mock_sftp = MagicMock()
                        mock_ssh.open_sftp.return_value = mock_sftp

                        result = ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                            port=65535,
                        )
                        assert result["success"] is True


def test_ssh_copy_file_type_error_local_path() -> None:
    """
    Test case 8: Test TypeError for invalid local_path type.
    """
    with pytest.raises(TypeError, match="local_path must be a string"):
        ssh_copy_file(123, "/remote/path.txt", "host")


def test_ssh_copy_file_type_error_remote_path() -> None:
    """
    Test case 9: Test TypeError for invalid remote_path type.
    """
    with pytest.raises(TypeError, match="remote_path must be a string"):
        ssh_copy_file("local.txt", 123, "host")


def test_ssh_copy_file_type_error_host() -> None:
    """
    Test case 10: Test TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_copy_file("local.txt", "/remote/path.txt", 123)


def test_ssh_copy_file_type_error_user() -> None:
    """
    Test case 11: Test TypeError for invalid user type.
    """
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", user=123)


def test_ssh_copy_file_type_error_password() -> None:
    """
    Test case 12: Test TypeError for invalid password type.
    """
    with pytest.raises(TypeError, match="password must be a string or None"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", password=123)


def test_ssh_copy_file_type_error_key_filename() -> None:
    """
    Test case 13: Test TypeError for invalid key_filename type.
    """
    with pytest.raises(TypeError, match="key_filename must be a string or None"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", key_filename=123)


def test_ssh_copy_file_type_error_port() -> None:
    """
    Test case 14: Test TypeError for invalid port type.
    """
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port="22")


def test_ssh_copy_file_type_error_timeout() -> None:
    """
    Test case 15: Test TypeError for invalid timeout type.
    """
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout="30")


def test_ssh_copy_file_value_error_port_too_low() -> None:
    """
    Test case 16: Test ValueError for port value too low.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port=0)


def test_ssh_copy_file_value_error_port_too_high() -> None:
    """
    Test case 17: Test ValueError for port value too high.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port=70000)


def test_ssh_copy_file_value_error_timeout_negative() -> None:
    """
    Test case 18: Test ValueError for negative timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout=-5)


def test_ssh_copy_file_value_error_timeout_zero() -> None:
    """
    Test case 19: Test ValueError for zero timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout=0)


def test_ssh_copy_file_value_error_file_not_found() -> None:
    """
    Test case 20: Test ValueError when local file doesn't exist.
    """
    with patch("ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=False):
        with pytest.raises(ValueError, match="Local file not found"):
            ssh_copy_file(
                "nonexistent.txt",
                "/remote/path.txt",
                "host",
                user="user",
                password="pass",
            )


def test_ssh_copy_file_value_error_not_a_file() -> None:
    """
    Test case 21: Test ValueError when local path is not a file.
    """
    with patch("ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True):
        with patch(
            "ssh_functions.remote.ssh_copy_file.os.path.isfile", return_value=False
        ):
            with pytest.raises(ValueError, match="Local path is not a file"):
                ssh_copy_file(
                    "/some/directory",
                    "/remote/path.txt",
                    "host",
                    user="user",
                    password="pass",
                )


def test_ssh_copy_file_runtime_error_auth_failure() -> None:
    """
    Test case 22: Test RuntimeError for authentication failure.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    mock_ssh = MagicMock()
                    mock_client.return_value = mock_ssh
                    import paramiko

                    mock_ssh.connect.side_effect = paramiko.AuthenticationException(
                        "Auth failed"
                    )

                    with pytest.raises(RuntimeError, match="SSH authentication failed"):
                        ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="badpass",
                        )


def test_ssh_copy_file_runtime_error_ssh_exception() -> None:
    """
    Test case 23: Test RuntimeError for SSH exception.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    mock_ssh = MagicMock()
                    mock_client.return_value = mock_ssh
                    import paramiko

                    mock_ssh.connect.side_effect = paramiko.SSHException("SSH error")

                    with pytest.raises(RuntimeError, match="SSH connection error"):
                        ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                        )


def test_ssh_copy_file_runtime_error_timeout() -> None:
    """
    Test case 24: Test RuntimeError for timeout.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    mock_ssh = MagicMock()
                    mock_client.return_value = mock_ssh
                    mock_ssh.connect.side_effect = TimeoutError("Transfer timed out")

                    with pytest.raises(RuntimeError, match="File transfer timed out"):
                        ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                        )


def test_ssh_copy_file_runtime_error_general() -> None:
    """
    Test case 25: Test RuntimeError for general exception.
    """
    with patch("ssh_functions.remote.ssh_copy_file.paramiko.SSHClient") as mock_client:
        with patch(
            "ssh_functions.remote.ssh_copy_file.getpass.getuser",
            return_value="testuser",
        ):
            with patch(
                "ssh_functions.remote.ssh_copy_file.os.path.exists", return_value=True
            ):
                with patch(
                    "ssh_functions.remote.ssh_copy_file.os.path.isfile",
                    return_value=True,
                ):
                    mock_ssh = MagicMock()
                    mock_client.return_value = mock_ssh
                    mock_ssh.open_sftp.side_effect = Exception("SFTP failed")

                    with pytest.raises(RuntimeError, match="File transfer failed"):
                        ssh_copy_file(
                            "local.txt",
                            "/remote/path.txt",
                            "host",
                            user="user",
                            password="pass",
                        )
