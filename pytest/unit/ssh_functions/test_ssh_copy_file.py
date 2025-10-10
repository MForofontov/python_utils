from unittest.mock import patch

import pytest
from ssh_functions.ssh_copy_file import ssh_copy_file


def test_ssh_copy_file_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = ssh_copy_file(
            "file.txt", "/tmp/file.txt", "host", user="user", port=22, timeout=5
        )
        assert result == {"stdout": "", "stderr": "", "exit_code": 0}


def test_ssh_copy_file_case_2_edge_case_empty_file() -> None:
    """
    Test case 2: Edge case with empty local file path.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result = ssh_copy_file("", "/tmp/file.txt", "host")
        assert result["exit_code"] == 0


def test_ssh_copy_file_case_5_boundary_conditions() -> None:
    """
    Test case 3: Boundary conditions for port.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0
        result_min = ssh_copy_file("file.txt", "/tmp/file.txt", "host", port=1)
        result_max = ssh_copy_file("file.txt", "/tmp/file.txt", "host", port=65535)
        assert result_min["exit_code"] == 0
        assert result_max["exit_code"] == 0


def test_ssh_copy_file_case_3_type_error_local_path() -> None:
    """
    Test case 4: TypeError for invalid local_path type.
    """
    with pytest.raises(TypeError, match="local_path must be a string"):
        ssh_copy_file(123, "/tmp/file.txt", "host")


def test_ssh_copy_file_case_4_value_error_port() -> None:
    """
    Test case 5: ValueError for invalid port value.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_copy_file("file.txt", "/tmp/file.txt", "host", port=70000)


def test_ssh_copy_file_case_6_timeout_error() -> None:
    """
    Test case 6: RuntimeError for timeout.
    """
    with patch("subprocess.run", side_effect=Exception("fail")):
        with pytest.raises(RuntimeError, match="SCP command failed: fail"):
            ssh_copy_file("file.txt", "/tmp/file.txt", "host")
