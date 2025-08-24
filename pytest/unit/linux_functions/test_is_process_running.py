import pytest
from linux_functions.is_process_running import is_process_running


def test_is_process_running_valid_process() -> None:
    """
    Test is_process_running function with a process that should exist.
    """
    # Test case 1: Check for init process (likely to exist on most systems)
    result: bool = is_process_running('init')
    assert isinstance(result, bool)


def test_is_process_running_nonexistent_process() -> None:
    """
    Test is_process_running function with a nonexistent process.
    """
    # Test case 2: Check for nonexistent process
    result: bool = is_process_running('nonexistent_process_12345')
    assert result == False


def test_is_process_running_invalid_type() -> None:
    """
    Test is_process_running function with invalid input type raises TypeError.
    """
    # Test case 3: Invalid type for process name
    with pytest.raises(TypeError):
        is_process_running(123)
    
    with pytest.raises(TypeError):
        is_process_running(None)
    
    with pytest.raises(TypeError):
        is_process_running(['process_name'])
