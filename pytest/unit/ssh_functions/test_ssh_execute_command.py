import subprocess
from unittest.mock import patch

import pytest
from ssh_functions.ssh_execute_command import ssh_execute_command


def test_ssh_execute_command_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "output\n"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = ssh_execute_command(
            "host", "echo hello", user="user", port=22, timeout=5
        )
        assert result == {"stdout": "output", "stderr": "", "exit_code": 0}


def test_ssh_execute_command_case_2_edge_case_empty_command() -> None:
    """
    Test case 2: Edge case with empty command.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = ssh_execute_command("host", "", user="user")
        assert result == {"stdout": "", "stderr": "", "exit_code": 0}


def test_ssh_execute_command_case_5_boundary_conditions() -> None:
    """
    Test case 3: Boundary conditions for port.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "ok"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result_min = ssh_execute_command("host", "ls", port=1)
        result_max = ssh_execute_command("host", "ls", port=65535)
        assert result_min["exit_code"] == 0
        assert result_max["exit_code"] == 0


def test_ssh_execute_command_case_3_type_error_host() -> None:
    """
    Test case 4: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_execute_command(123, "ls")


def test_ssh_execute_command_case_4_value_error_port() -> None:
    """
    Test case 5: ValueError for invalid port value.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_execute_command("host", "ls", port=70000)


def test_ssh_execute_command_case_6_timeout_error() -> None:
    """
    Test case 6: RuntimeError for timeout.
    """
    with patch("subprocess.run", side_effect=Exception("fail")):
        with pytest.raises(RuntimeError, match="SSH command failed: fail"):
            ssh_execute_command("host", "ls")


def test_ssh_execute_command_case_7_timeout_expired() -> None:
    """
    Test case 7: subprocess.TimeoutExpired raises RuntimeError with timeout-specific message.
    """
    with patch(
        "subprocess.run",
        side_effect=subprocess.TimeoutExpired(cmd=["ssh"], timeout=5),
    ):
        with pytest.raises(RuntimeError, match="SSH command timed out after 5 seconds"):
            ssh_execute_command("host", "ls", timeout=5)
