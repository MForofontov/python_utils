import pytest
from typing import Dict, Union
from linux_functions.get_memory_info import get_memory_info


def test_get_memory_info_returns_valid_dict() -> None:
    """
    Test case 1: Test the get_memory_info function returns a valid dictionary with memory information.
    """
    mem_info: Dict[str, Union[int, float]] = get_memory_info()
    
    # Check return type
    assert isinstance(mem_info, dict)
    
    # Check required keys
    required_keys: list[str] = ['total', 'available', 'used', 'free', 'percent_used']
    for key in required_keys:
        assert key in mem_info
    
    # Check values are reasonable
    assert mem_info['total'] > 0
    assert mem_info['available'] >= 0
    assert mem_info['used'] >= 0
    assert mem_info['free'] >= 0
    assert 0 <= mem_info['percent_used'] <= 100
    
    # Check relationships
    assert mem_info['used'] <= mem_info['total']
    assert mem_info['available'] <= mem_info['total']
