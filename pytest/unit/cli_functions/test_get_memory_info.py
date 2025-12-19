import pytest
from cli_functions.get_memory_info import get_memory_info


def test_get_memory_info_case_1_returns_valid_dict() -> None:
    """
    Test case 1: Test get_memory_info returns valid dictionary.
    """
    mem_info = get_memory_info()
    
    assert isinstance(mem_info, dict)
    assert 'total' in mem_info
    assert 'available' in mem_info
    assert 'used' in mem_info
    assert 'free' in mem_info
    assert 'percent_used' in mem_info


def test_get_memory_info_case_2_positive_values() -> None:
    """
    Test case 2: Test all memory values are non-negative.
    """
    mem_info = get_memory_info()
    
    assert mem_info['total'] > 0
    assert mem_info['available'] >= 0
    assert mem_info['used'] >= 0
    assert mem_info['free'] >= 0


def test_get_memory_info_case_3_percent_range() -> None:
    """
    Test case 3: Test percent_used is in valid range.
    """
    mem_info = get_memory_info()
    assert 0 <= mem_info['percent_used'] <= 100


def test_get_memory_info_case_4_relationships() -> None:
    """
    Test case 4: Test relationships between memory values.
    """
    mem_info = get_memory_info()
    
    # Used should not exceed total
    assert mem_info['used'] <= mem_info['total']
    # Available should not exceed total
    assert mem_info['available'] <= mem_info['total']


def test_get_memory_info_case_5_consistency() -> None:
    """
    Test case 5: Test consistency between multiple calls.
    """
    mem_info1 = get_memory_info()
    mem_info2 = get_memory_info()
    
    # Total should be the same
    assert mem_info1['total'] == mem_info2['total']


def test_get_memory_info_case_6_value_types() -> None:
    """
    Test case 6: Test all values are correct types.
    """
    mem_info = get_memory_info()
    
    assert isinstance(mem_info['total'], int)
    assert isinstance(mem_info['used'], int)
    assert isinstance(mem_info['free'], int)
    assert isinstance(mem_info['percent_used'], (int, float))
