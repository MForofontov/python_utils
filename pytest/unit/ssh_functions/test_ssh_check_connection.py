from unittest.mock import patch

import pytest
from ssh_functions.ssh_check_connection import ssh_check_connection


def test_ssh_check_connection_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = ssh_check_connection("host", user="user", port=22, timeout=5)
        assert result == {"success": True, "stdout": "", "stderr": "", "exit_code": 0}


def test_ssh_check_connection_empty_user() -> None:
    """
    Test case 2: Edge case with empty user.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = ssh_check_connection("host", user="", port=22)
        assert result["success"] is True


def test_ssh_check_connection_boundary_conditions_port() -> None:
    """
    Test case 3: Boundary conditions for port.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result_min = ssh_check_connection("host", port=1)
        result_max = ssh_check_connection("host", port=65535)
        assert result_min["success"] is True
        assert result_max["success"] is True


def test_ssh_check_connection_type_error_host() -> None:
    """
    Test case 4: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_check_connection(123)


def test_ssh_check_connection_value_error_port() -> None:
    """
    Test case 5: ValueError for invalid port value.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_check_connection("host", port=70000)


def test_ssh_check_connection_timeout_error() -> None:
    """
    Test case 6: RuntimeError for timeout.
    """
    with patch("subprocess.run", side_effect=Exception("fail")):
        with pytest.raises(RuntimeError, match="SSH connection failed: fail"):
            ssh_check_connection("host")
