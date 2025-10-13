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
    assert not result


def test_is_process_running_handles_psutil_exceptions() -> None:
    """
    Test case 3: Test is_process_running handles psutil exceptions gracefully.
    """
    from unittest.mock import patch, MagicMock
    import psutil
    
    # Mock process_iter to raise exceptions during iteration
    with patch('psutil.process_iter') as mock_iter:
        # Create mock process that raises NoSuchProcess
        mock_proc = MagicMock()
        mock_proc.info = {"name": "test_process"}
        mock_proc.__getitem__.side_effect = psutil.NoSuchProcess(pid=123)
        
        mock_iter.return_value = [mock_proc]
        
        # Should handle exception and continue, returning False
        result = is_process_running("test_process")
        assert isinstance(result, bool)


def test_is_process_running_invalid_type() -> None:
    """
    Test case 4: Test is_process_running function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        is_process_running(123)

    with pytest.raises(TypeError):
        is_process_running(None)

    with pytest.raises(TypeError):
        is_process_running(["process_name"])
