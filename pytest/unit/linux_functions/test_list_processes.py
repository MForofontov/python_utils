import pytest
from typing import List, Dict, Any
from linux_functions.list_processes import list_processes


def test_list_processes_returns_valid_list() -> None:
    """
    Test the list_processes function returns a valid list of process information.
    """
    # Test case 1: Get list of running processes
    processes: List[Dict[str, Any]] = list_processes()
    
    # Check return type
    assert isinstance(processes, list)
    
    # Should have at least some processes running
    assert len(processes) > 0
    
    # Check structure of first process
    if processes:
        process: Dict[str, Any] = processes[0]
        assert isinstance(process, dict)
        
        # Check for expected keys
        expected_keys: list[str] = ['pid', 'name']
        for key in expected_keys:
            assert key in process
        
        # Check pid is integer
        assert isinstance(process['pid'], int)
        assert process['pid'] > 0
        
        # Check name is string or None
        assert isinstance(process['name'], (str, type(None)))
