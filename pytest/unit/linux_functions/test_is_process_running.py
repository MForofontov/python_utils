import pytest
from linux_functions.is_process_running import is_process_running


def test_is_process_running_valid_process() -> None:
    """
    Test case 1: Test is_process_running function with a process that should exist.
    """
    result: bool = is_process_running("init")
    assert isinstance(result, bool)


def test_is_process_running_nonexistent_process() -> None:
    """
    Test case 2: Test is_process_running function with a nonexistent process.
    """
    result: bool = is_process_running("nonexistent_process_12345")
    assert result == False


def test_is_process_running_invalid_type() -> None:
    """
    Test case 3: Test is_process_running function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        is_process_running(123)

    with pytest.raises(TypeError):
        is_process_running(None)

    with pytest.raises(TypeError):
        is_process_running(["process_name"])
