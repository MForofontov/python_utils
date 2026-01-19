"""Tests for local SSH execute script using subprocess."""

import subprocess
from unittest.mock import MagicMock, mock_open, patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.ssh_functions]
from ssh_functions.local.ssh_execute_script import ssh_execute_script


def test_ssh_execute_script_successful() -> None:
    """
    Test case 1: Successful script execution.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\necho hello")):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="hello", stderr="", returncode=0)
            result = ssh_execute_script("host", "script.sh", user="user")
            assert result["stdout"] == "hello"
            assert result["exit_code"] == 0


def test_ssh_execute_script_with_stderr() -> None:
    """
    Test case 2: Script execution with stderr output.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\necho error >&2")):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="", stderr="error", returncode=1)
            result = ssh_execute_script("host", "script.sh", user="user")
            assert result["stderr"] == "error"
            assert result["exit_code"] == 1


def test_ssh_execute_script_with_custom_port() -> None:
    """
    Test case 3: Script execution with custom port.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\nls")):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="ok", stderr="", returncode=0)
            result = ssh_execute_script("host", "script.sh", user="user", port=2222)
            assert result["exit_code"] == 0


def test_ssh_execute_script_without_user() -> None:
    """
    Test case 4: Script execution without specifying user.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\nls")):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="ok", stderr="", returncode=0)
            result = ssh_execute_script("host", "script.sh")
            assert result["exit_code"] == 0


def test_ssh_execute_script_boundary_port_min() -> None:
    """
    Test case 5: Script execution with minimum port value.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\nls")):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="ok", stderr="", returncode=0)
            result = ssh_execute_script("host", "script.sh", port=1)
            assert result["exit_code"] == 0


def test_ssh_execute_script_boundary_port_max() -> None:
    """
    Test case 6: Script execution with maximum port value.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\nls")):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="ok", stderr="", returncode=0)
            result = ssh_execute_script("host", "script.sh", port=65535)
            assert result["exit_code"] == 0


def test_ssh_execute_script_type_error_host() -> None:
    """
    Test case 7: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_execute_script(123, "script.sh")


def test_ssh_execute_script_type_error_script_path() -> None:
    """
    Test case 8: TypeError for invalid script_path type.
    """
    with pytest.raises(TypeError, match="script_path must be a string"):
        ssh_execute_script("host", 123)


def test_ssh_execute_script_type_error_user() -> None:
    """
    Test case 9: TypeError for invalid user type.
    """
    with pytest.raises(TypeError, match="user must be a string or None"):
        ssh_execute_script("host", "script.sh", user=123)


def test_ssh_execute_script_type_error_port() -> None:
    """
    Test case 10: TypeError for invalid port type.
    """
    with pytest.raises(TypeError, match="port must be an integer"):
        ssh_execute_script("host", "script.sh", port="22")


def test_ssh_execute_script_type_error_timeout() -> None:
    """
    Test case 11: TypeError for invalid timeout type.
    """
    with pytest.raises(TypeError, match="timeout must be a number"):
        ssh_execute_script("host", "script.sh", timeout="60")


def test_ssh_execute_script_value_error_port_too_low() -> None:
    """
    Test case 12: ValueError for port value too low.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_execute_script("host", "script.sh", port=0)


def test_ssh_execute_script_value_error_port_too_high() -> None:
    """
    Test case 13: ValueError for port value too high.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_execute_script("host", "script.sh", port=70000)


def test_ssh_execute_script_value_error_timeout_negative() -> None:
    """
    Test case 14: ValueError for negative timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_execute_script("host", "script.sh", timeout=-5)


def test_ssh_execute_script_value_error_timeout_zero() -> None:
    """
    Test case 15: ValueError for zero timeout.
    """
    with pytest.raises(ValueError, match="timeout must be positive"):
        ssh_execute_script("host", "script.sh", timeout=0)


def test_ssh_execute_script_value_error_file_not_found() -> None:
    """
    Test case 16: ValueError when script file not found.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(ValueError, match="Script file not found"):
            ssh_execute_script("host", "nonexistent.sh")


def test_ssh_execute_script_runtime_error_timeout() -> None:
    """
    Test case 17: RuntimeError when script execution times out.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\nsleep 100")):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("ssh", 60)
            with pytest.raises(RuntimeError, match="SSH command timed out"):
                ssh_execute_script("host", "script.sh")


def test_ssh_execute_script_runtime_error_general() -> None:
    """
    Test case 18: RuntimeError for general subprocess failure.
    """
    with patch("builtins.open", mock_open(read_data=b"#!/bin/bash\nls")):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Connection failed")
            with pytest.raises(RuntimeError, match="SSH command failed"):
                ssh_execute_script("host", "script.sh")
