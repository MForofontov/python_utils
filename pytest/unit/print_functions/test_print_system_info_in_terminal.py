from unittest.mock import patch

import pytest

try:
    import psutil
    from pyutils_collection.print_functions.print_system_info_in_terminal import print_system_info_in_terminal
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None  # type: ignore
    print_system_info_in_terminal = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.print_functions,
    pytest.mark.skipif(not PSUTIL_AVAILABLE, reason="psutil not installed"),
]


def test_print_system_info_in_terminal_basic(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Test case 1: Prints basic system info and separator.
    """
    with (
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.cpu_count",
            return_value=4,
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.virtual_memory"
        ) as mock_vm,
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.disk_usage",
            return_value=type("DU", (), {"percent": 50})(),
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.boot_time",
            return_value=0,
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.platform.processor",
            return_value="TestProcessor",
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.shutil.get_terminal_size",
            return_value=type("TS", (), {"columns": 80})(),
        ),
    ):
        mock_vm.return_value.total = 8 * 1024 * 1024
        mock_vm.return_value.available = 4 * 1024 * 1024
        print_system_info_in_terminal()
        out = capsys.readouterr().out
        assert "System Information" in out
        assert "Operating System:" in out
        assert "CPU count:" in out
        assert "Total memory:" in out
        assert "Disk usage:" in out
        assert "System Uptime:" in out
        assert "=" in out


def test_print_system_info_in_terminal_lscpu_failure(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Test case 2: Test fallback to platform.processor() when lscpu fails.
    """
    with (
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.cpu_count",
            return_value=2,
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.virtual_memory"
        ) as mock_vm,
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.disk_usage",
            return_value=type("DU", (), {"percent": 25})(),
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.boot_time",
            return_value=1000,
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.platform.processor",
            return_value="FallbackProcessor",
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.shutil.get_terminal_size",
            return_value=type("TS", (), {"columns": 100})(),
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.subprocess.run",
            side_effect=FileNotFoundError("lscpu not found"),
        ),
    ):
        mock_vm.return_value.total = 16 * 1024 * 1024
        mock_vm.return_value.available = 8 * 1024 * 1024
        print_system_info_in_terminal()
        out = capsys.readouterr().out
        assert "FallbackProcessor" in out
        assert "CPU count:" in out


def test_print_system_info_in_terminal_lscpu_without_model_name(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    Test case 3: Test when lscpu succeeds but doesn't contain 'Model name'.
    """
    with (
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.cpu_count",
            return_value=8,
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.virtual_memory"
        ) as mock_vm,
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.disk_usage",
            return_value=type("DU", (), {"percent": 75})(),
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.psutil.boot_time",
            return_value=500,
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.platform.processor",
            return_value="GenericProcessor",
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.shutil.get_terminal_size",
            return_value=type("TS", (), {"columns": 120})(),
        ),
        patch(
            "python_utils.print_functions.print_system_info_in_terminal.subprocess.run",
            return_value=type(
                "Result",
                (),
                {"stdout": "Architecture: x86_64\nCPU op-mode(s): 32-bit, 64-bit"},
            )(),
        ),
    ):
        mock_vm.return_value.total = 32 * 1024 * 1024
        mock_vm.return_value.available = 16 * 1024 * 1024
        print_system_info_in_terminal()
        out = capsys.readouterr().out
        assert "GenericProcessor" in out
        assert "CPU count:" in out
