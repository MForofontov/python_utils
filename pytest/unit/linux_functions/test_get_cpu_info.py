import pytest
from typing import Dict, Union, List
from linux_functions.get_cpu_info import get_cpu_info


@pytest.mark.parametrize("interval", [None, 0.05])
def test_get_cpu_info_returns_valid_dict(interval: float | None) -> None:
    """Test the get_cpu_info function returns a valid dictionary with CPU information."""
    cpu_info: Dict[str, Union[int, float, List[float]]]
    if interval is None:
        cpu_info = get_cpu_info()
    else:
        cpu_info = get_cpu_info(interval=interval)
    
    # Check return type
    assert isinstance(cpu_info, dict)
    
    # Check required keys
    required_keys: list[str] = ['cpu_count', 'cpu_percent', 'cpu_percent_per_core']
    for key in required_keys:
        assert key in cpu_info
    
    # Check cpu_count
    assert isinstance(cpu_info['cpu_count'], int)
    assert cpu_info['cpu_count'] > 0
    
    # Check cpu_percent
    assert isinstance(cpu_info['cpu_percent'], (int, float))
    assert 0 <= cpu_info['cpu_percent'] <= 100
    
    # Check cpu_percent_per_core
    assert isinstance(cpu_info['cpu_percent_per_core'], list)
    assert len(cpu_info['cpu_percent_per_core']) == cpu_info['cpu_count']
    
    per_core_percents: List[float] = cpu_info['cpu_percent_per_core']
    for core_percent in per_core_percents:
        assert isinstance(core_percent, (int, float))
        assert 0 <= core_percent <= 100
