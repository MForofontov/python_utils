"""
Module for listing running processes.
"""

import psutil
from typing import List, Dict, Any


def list_processes() -> List[Dict[str, Any]]:
    """
    Get list of running processes with their information.

    Returns
    -------
    List[Dict[str, Any]]
        List of dictionaries containing process information.

    Examples
    --------
    >>> processes = list_processes()
    >>> len(processes) > 0
    True
    >>> 'pid' in processes[0]
    True
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process might have terminated or we don't have permission
            continue
    
    return processes
