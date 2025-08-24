"""
Module for getting CPU information.
"""

import psutil
import os
from typing import Dict, Union, List


def get_cpu_info() -> Dict[str, Union[int, float, List[float]]]:
    """
    Get CPU information and usage statistics.

    Returns
    -------
    Dict[str, Union[int, float, List[float]]]
        Dictionary containing CPU information including count, usage, and frequencies.

    Examples
    --------
    >>> cpu_info = get_cpu_info()
    >>> 'cpu_count' in cpu_info
    True
    >>> cpu_info['cpu_count'] > 0
    True
    """
    return {
        'cpu_count': os.cpu_count(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'cpu_percent_per_core': psutil.cpu_percent(interval=1, percpu=True),
        'cpu_freq_current': psutil.cpu_freq().current if psutil.cpu_freq() else None,
        'cpu_freq_min': psutil.cpu_freq().min if psutil.cpu_freq() else None,
        'cpu_freq_max': psutil.cpu_freq().max if psutil.cpu_freq() else None,
        'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
    }
