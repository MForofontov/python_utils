import pytest
from linux_functions.kill_process import kill_process


def test_kill_process_nonexistent_pid() -> None:
    """
    Test case 1: Test kill_process function with a nonexistent PID returns False.
    """
    result: bool = kill_process(999999)
    assert result == False


def test_kill_process_invalid_type() -> None:
    """
    Test case 2: Test kill_process function with invalid input types raises TypeError.
    """
    with pytest.raises(TypeError):
        kill_process("123")
    
    with pytest.raises(TypeError):
        kill_process(None)
    
    with pytest.raises(TypeError):
        kill_process(12.5)


def test_kill_process_invalid_pid() -> None:
    """
    Test case 3: Test kill_process function with invalid PID values raises ValueError.
    """
    with pytest.raises(ValueError):
        kill_process(0)
    
    with pytest.raises(ValueError):
        kill_process(-1)
    
    with pytest.raises(ValueError):
        kill_process(-999)
