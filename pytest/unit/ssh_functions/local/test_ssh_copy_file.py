"""Tests for local SSH copy file using subprocess."""

import pytest

try:
    import subprocess
    from unittest.mock import MagicMock, patch
    import paramiko
    from pyutils_collection.ssh_functions.local.ssh_copy_file import ssh_copy_file
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    subprocess = None  # type: ignore
    MagicMock = None  # type: ignore
    patch = None  # type: ignore
    paramiko = None  # type: ignore
    ssh_copy_file = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.ssh_functions,
    pytest.mark.skipif(not PARAMIKO_AVAILABLE, reason="paramiko not installed"),
]


def test_ssh_copy_file_successful() -> None:
    """
    Test case 1: Successful file copy.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", user="user")
        assert result["exit_code"] == 0


def test_ssh_copy_file_with_stderr() -> None:
    """
    Test case 2: File copy with stderr output.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="warning", returncode=0)
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", user="user")
        assert result["stderr"] == "warning"


def test_ssh_copy_file_with_custom_port() -> None:
    """
    Test case 3: File copy with custom port.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_copy_file(
            "local.txt", "/remote/path.txt", "host", user="user", port=2222
        )
        assert result["exit_code"] == 0


def test_ssh_copy_file_without_user() -> None:
    """
    Test case 4: File copy without specifying user.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host")
        assert result["exit_code"] == 0


def test_ssh_copy_file_boundary_port_min() -> None:
    """
    Test case 5: File copy with minimum port value.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", port=1)
        assert result["exit_code"] == 0


def test_ssh_copy_file_boundary_port_max() -> None:
    """
    Test case 6: File copy with maximum port value.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="", returncode=0)
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", port=65535)
        assert result["exit_code"] == 0


def test_ssh_copy_file_type_error_local_path() -> None:
    """
    Test case 7: TypeError for invalid local_path type.
    """
    with pytest.raises(TypeError, match="local_path must be a string"):
        ssh_copy_file(123, "/remote/path.txt", "host")


def test_ssh_copy_file_type_error_remote_path() -> None:
    """
    Test case 8: TypeError for invalid remote_path type.
    """
    with pytest.raises(TypeError, match="remote_path must be a string"):
        ssh_copy_file("local.txt", 123, "host")


def test_ssh_copy_file_type_error_host() -> None:
    """
    Test case 9: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_copy_file("local.txt", "/remote/path.txt", 123)


def test_ssh_copy_file_type_error_user() -> None:
    """
    Test case 10: TypeError for invalid user type.
    """
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", user=123)


def test_ssh_copy_file_type_error_port() -> None:
    """
    Test case 11: TypeError for invalid port type.
    """
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port="22")


def test_ssh_copy_file_type_error_timeout() -> None:
    """
    Test case 12: TypeError for invalid timeout type.
    """
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout="30")


def test_ssh_copy_file_value_error_port_too_low() -> None:
    """
    Test case 13: ValueError for port value too low.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port=0)


def test_ssh_copy_file_value_error_port_too_high() -> None:
    """
    Test case 14: ValueError for port value too high.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port=70000)


def test_ssh_copy_file_value_error_timeout_negative() -> None:
    """
    Test case 15: ValueError for negative timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout=-5)


def test_ssh_copy_file_value_error_timeout_zero() -> None:
    """
    Test case 16: ValueError for zero timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout=0)


def test_ssh_copy_file_runtime_error_timeout() -> None:
    """
    Test case 17: RuntimeError when file copy times out.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired("scp", 30)
        with pytest.raises(RuntimeError, match="SCP command timed out"):
            ssh_copy_file("local.txt", "/remote/path.txt", "host")


def test_ssh_copy_file_runtime_error_general() -> None:
    """
    Test case 18: RuntimeError for general subprocess failure.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("Transfer failed")
        with pytest.raises(RuntimeError, match="SCP command failed"):
            ssh_copy_file("local.txt", "/remote/path.txt", "host")
