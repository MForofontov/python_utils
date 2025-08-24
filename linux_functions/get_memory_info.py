"""
Module for getting memory information.
"""

import psutil
from typing import Dict, Union


def get_memory_info() -> Dict[str, Union[int, float]]:
    """
    Get system memory information.

    Returns
    -------
    Dict[str, Union[int, float]]
        Dictionary containing memory information in bytes and percentage.

    Examples
    --------
    >>> mem_info = get_memory_info()
    >>> 'total' in mem_info
    True
    >>> mem_info['total'] > 0
    True
    """
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'free': memory.free,
        'percent_used': memory.percent
    }
