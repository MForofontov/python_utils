"""Tests for local SSH execute command using subprocess."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from ssh_functions.local.ssh_execute_command import ssh_execute_command


def test_ssh_execute_command_successful_execution() -> None:
    """Test successful command execution."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="output", stderr="", returncode=0
        )
        result = ssh_execute_command("host", "ls /tmp", user="user")
        assert result["stdout"] == "output"
        assert result["stderr"] == ""
        assert result["exit_code"] == 0


def test_ssh_execute_command_with_stderr() -> None:
    """Test command execution with stderr output."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="", stderr="error", returncode=1
        )
        result = ssh_execute_command("host", "bad_command", user="user")
        assert result["stderr"] == "error"
        assert result["exit_code"] == 1


def test_ssh_execute_command_with_custom_port() -> None:
    """Test command execution with custom port."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="ok", stderr="", returncode=0
        )
        result = ssh_execute_command("host", "ls", user="user", port=2222)
        assert result["exit_code"] == 0
        mock_run.assert_called_once()


def test_ssh_execute_command_without_user() -> None:
    """Test command execution without specifying user."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="ok", stderr="", returncode=0
        )
        result = ssh_execute_command("host", "ls")
        assert result["exit_code"] == 0


def test_ssh_execute_command_boundary_port_min() -> None:
    """Test command execution with minimum port value."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="ok", stderr="", returncode=0
        )
        result = ssh_execute_command("host", "ls", port=1)
        assert result["exit_code"] == 0


def test_ssh_execute_command_boundary_port_max() -> None:
    """Test command execution with maximum port value."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout="ok", stderr="", returncode=0
        )
        result = ssh_execute_command("host", "ls", port=65535)
        assert result["exit_code"] == 0


def test_ssh_execute_command_type_error_host() -> None:
    """Test TypeError for invalid host type."""
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_execute_command(123, "ls")


def test_ssh_execute_command_type_error_command() -> None:
    """Test TypeError for invalid command type."""
    with pytest.raises(TypeError, match="command must be a string"):
        ssh_execute_command("host", 123)


def test_ssh_execute_command_type_error_user() -> None:
    """Test TypeError for invalid user type."""
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_execute_command("host", "ls", user=123)


def test_ssh_execute_command_type_error_port() -> None:
    """Test TypeError for invalid port type."""
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_execute_command("host", "ls", port="22")


def test_ssh_execute_command_type_error_timeout() -> None:
    """Test TypeError for invalid timeout type."""
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_execute_command("host", "ls", timeout="30")


def test_ssh_execute_command_value_error_port_too_low() -> None:
    """Test ValueError for port value too low."""
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_execute_command("host", "ls", port=0)


def test_ssh_execute_command_value_error_port_too_high() -> None:
    """Test ValueError for port value too high."""
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_execute_command("host", "ls", port=70000)


def test_ssh_execute_command_value_error_timeout_negative() -> None:
    """Test ValueError for negative timeout."""
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_execute_command("host", "ls", timeout=-5)


def test_ssh_execute_command_value_error_timeout_zero() -> None:
    """Test ValueError for zero timeout."""
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_execute_command("host", "ls", timeout=0)


def test_ssh_execute_command_runtime_error_timeout() -> None:
    """Test RuntimeError when command times out."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired("ssh", 30)
        with pytest.raises(RuntimeError, match="SSH command timed out"):
            ssh_execute_command("host", "ls")


def test_ssh_execute_command_runtime_error_general() -> None:
    """Test RuntimeError for general subprocess failure."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("Connection failed")
        with pytest.raises(RuntimeError, match="SSH command failed"):
            ssh_execute_command("host", "ls")
