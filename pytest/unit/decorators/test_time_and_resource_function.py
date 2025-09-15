import pytest
import logging
import time
from decorators.time_and_resource_function import time_and_resource_function

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Sample function to be decorated
@time_and_resource_function()
def sample_function() -> str:
    time.sleep(1)
    return "Function executed"


def test_time_and_resource_function_success(capfd):
    """
    Test case 1: Function executes successfully and prints time and resource usage
    """
    result = sample_function()
    assert result == "Function executed"
    captured = capfd.readouterr()
    assert "Execution time" in captured.out


def test_time_and_resource_function_with_logger(caplog):
    """
    Test case 2: Function executes successfully with logger
    """

    @time_and_resource_function(logger=test_logger)
    def function_with_logger() -> str:
        time.sleep(1)
        return "Function executed"

    with caplog.at_level(logging.DEBUG):
        result = function_with_logger()
        assert result == "Function executed"
        assert "Execution time" in caplog.text


def test_time_and_resource_function_with_all_monitors(capfd):
    """
    Test case 3: Function executes successfully with all monitors enabled
    """

    @time_and_resource_function(
        monitor_memory=True,
        monitor_cpu=True,
        monitor_io=True,
        monitor_network=True,
        monitor_disk=True,
        monitor_threads=True,
        monitor_gc=True,
        monitor_context_switches=True,
        monitor_open_files=True,
        monitor_page_faults=True,
    )
    def function_with_all_monitors() -> str:
        time.sleep(1)
        return "Function executed"

    result = function_with_all_monitors()
    assert result == "Function executed"
    captured = capfd.readouterr()
    assert "Execution time" in captured.out
    assert "Maximum memory usage" in captured.out
    assert "Maximum CPU usage" in captured.out
    assert "Read operations" in captured.out
    assert "Write operations" in captured.out
    assert "Bytes sent" in captured.out
    assert "Bytes received" in captured.out
    assert "Disk read bytes" in captured.out
    assert "Disk write bytes" in captured.out
    assert "Number of threads" in captured.out
    assert "GC collections" in captured.out
    assert "Voluntary context switches" in captured.out
    assert "Involuntary context switches" in captured.out
    assert "Maximum open files" in captured.out
    assert "Maximum page faults" in captured.out


def test_time_and_resource_function_prints(capfd):
    """
    Test case 4: Function executes successfully and prints time and resource usage
    """

    @time_and_resource_function(
        monitor_memory=True,
        monitor_cpu=True,
        monitor_io=True,
        monitor_network=True,
        monitor_disk=True,
        monitor_threads=True,
        monitor_gc=True,
        monitor_context_switches=True,
        monitor_open_files=True,
        monitor_page_faults=True,
    )
    def function_with_all_monitors_prints() -> str:
        time.sleep(1)
        return "Function executed"

    result = function_with_all_monitors_prints()
    assert result == "Function executed"

    captured = capfd.readouterr()
    assert "Execution time" in captured.out
    assert "Maximum memory usage" in captured.out
    assert "Maximum CPU usage" in captured.out
    assert "Read operations" in captured.out
    assert "Write operations" in captured.out
    assert "Bytes sent" in captured.out
    assert "Bytes received" in captured.out
    assert "Disk read bytes" in captured.out
    assert "Disk write bytes" in captured.out
    assert "Number of threads" in captured.out
    assert "GC collections" in captured.out
    assert "Voluntary context switches" in captured.out
    assert "Involuntary context switches" in captured.out
    assert "Maximum open files" in captured.out
    assert "Maximum page faults" in captured.out


def test_invalid_logger_type():
    """
    Test case 5: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @time_and_resource_function(logger="not_a_logger")
        def invalid_logger_function() -> None:
            pass
