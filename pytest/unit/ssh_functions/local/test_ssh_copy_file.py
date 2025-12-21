"""Tests for local SSH copy file using subprocess."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from ssh_functions.local.ssh_copy_file import ssh_copy_file


def test_ssh_copy_file_successful() -> None:
    """Test successful file copy."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="", returncode=0
        )
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", user="user")
        assert result["exit_code"] == 0


def test_ssh_copy_file_with_stderr() -> None:
    """Test file copy with stderr output."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="warning", returncode=0
        )
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", user="user")
        assert result["stderr"] == "warning"


def test_ssh_copy_file_with_custom_port() -> None:
    """Test file copy with custom port."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="", returncode=0
        )
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", user="user", port=2222)
        assert result["exit_code"] == 0


def test_ssh_copy_file_without_user() -> None:
    """Test file copy without specifying user."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="", returncode=0
        )
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host")
        assert result["exit_code"] == 0


def test_ssh_copy_file_boundary_port_min() -> None:
    """Test file copy with minimum port value."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="", returncode=0
        )
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", port=1)
        assert result["exit_code"] == 0


def test_ssh_copy_file_boundary_port_max() -> None:
    """Test file copy with maximum port value."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="", returncode=0
        )
        result = ssh_copy_file("local.txt", "/remote/path.txt", "host", port=65535)
        assert result["exit_code"] == 0


def test_ssh_copy_file_type_error_local_path() -> None:
    """Test TypeError for invalid local_path type."""
    with pytest.raises(TypeError, match="local_path must be a string"):
        ssh_copy_file(123, "/remote/path.txt", "host")


def test_ssh_copy_file_type_error_remote_path() -> None:
    """Test TypeError for invalid remote_path type."""
    with pytest.raises(TypeError, match="remote_path must be a string"):
        ssh_copy_file("local.txt", 123, "host")


def test_ssh_copy_file_type_error_host() -> None:
    """Test TypeError for invalid host type."""
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_copy_file("local.txt", "/remote/path.txt", 123)


def test_ssh_copy_file_type_error_user() -> None:
    """Test TypeError for invalid user type."""
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", user=123)


def test_ssh_copy_file_type_error_port() -> None:
    """Test TypeError for invalid port type."""
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port="22")


def test_ssh_copy_file_type_error_timeout() -> None:
    """Test TypeError for invalid timeout type."""
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout="30")


def test_ssh_copy_file_value_error_port_too_low() -> None:
    """Test ValueError for port value too low."""
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port=0)


def test_ssh_copy_file_value_error_port_too_high() -> None:
    """Test ValueError for port value too high."""
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", port=70000)


def test_ssh_copy_file_value_error_timeout_negative() -> None:
    """Test ValueError for negative timeout."""
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout=-5)


def test_ssh_copy_file_value_error_timeout_zero() -> None:
    """Test ValueError for zero timeout."""
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_copy_file("local.txt", "/remote/path.txt", "host", timeout=0)


def test_ssh_copy_file_runtime_error_timeout() -> None:
    """Test RuntimeError when file copy times out."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired("scp", 30)
        with pytest.raises(RuntimeError, match="SCP command timed out"):
            ssh_copy_file("local.txt", "/remote/path.txt", "host")


def test_ssh_copy_file_runtime_error_general() -> None:
    """Test RuntimeError for general subprocess failure."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("Transfer failed")
        with pytest.raises(RuntimeError, match="SCP command failed"):
            ssh_copy_file("local.txt", "/remote/path.txt", "host")
