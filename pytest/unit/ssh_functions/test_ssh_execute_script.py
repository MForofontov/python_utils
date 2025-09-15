import pytest
from unittest.mock import patch, mock_open
from ssh_functions.ssh_execute_script import ssh_execute_script


def test_ssh_execute_script_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    m = mock_open(read_data=b"echo hello")
    with patch("builtins.open", m):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = "result"
            mock_run.return_value.stderr = ""
            mock_run.return_value.returncode = 0
            result = ssh_execute_script(
                "host", "myscript.sh", user="user", port=22, timeout=5
            )
            assert result == {"stdout": "result", "stderr": "", "exit_code": 0}


def test_ssh_execute_script_case_2_edge_case_empty_script() -> None:
    """
    Test case 2: Edge case with empty script file.
    """
    m = mock_open(read_data=b"")
    with patch("builtins.open", m):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = ""
            mock_run.return_value.returncode = 0
            result = ssh_execute_script("host", "myscript.sh")
            assert result["exit_code"] == 0


def test_ssh_execute_script_case_3_type_error_host() -> None:
    """
    Test case 3: TypeError for invalid host type.
    """
    with pytest.raises(TypeError, match="host must be a string"):
        ssh_execute_script(123, "myscript.sh")


def test_ssh_execute_script_case_4_value_error_port() -> None:
    """
    Test case 4: ValueError for invalid port value.
    """
    with pytest.raises(ValueError, match="port must be in 1-65535"):
        ssh_execute_script("host", "myscript.sh", port=70000)


def test_ssh_execute_script_case_5_file_not_found() -> None:
    """
    Test case 5: ValueError for missing script file.
    """
    with pytest.raises(ValueError, match="Script file not found"):
        ssh_execute_script("host", "notfound.sh")


def test_ssh_execute_script_case_6_timeout_error() -> None:
    """
    Test case 6: RuntimeError for timeout.
    """
    m = mock_open(read_data=b"echo hello")
    with patch("builtins.open", m):
        with patch("subprocess.run", side_effect=Exception("fail")):
            with pytest.raises(RuntimeError, match="SSH command failed: fail"):
                ssh_execute_script("host", "myscript.sh")
