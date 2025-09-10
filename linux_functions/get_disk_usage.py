"""
Module for getting disk usage information.
"""

import os
import psutil


def get_disk_usage(path: str = '/') -> dict[str, int | float]:
    """
    Get disk usage information for a given path.

    Parameters
    ----------
    path : str, optional
        Path to check disk usage for (by default '/').

    Returns
    -------
    dict[str, int | float]
        Dictionary containing disk usage information in bytes and percentage.

    Raises
    ------
    FileNotFoundError
        If path does not exist.
    TypeError
        If path is not a string.

    Examples
    --------
    >>> disk_info = get_disk_usage('/')
    >>> 'total' in disk_info
    True
    >>> disk_info['total'] > 0
    True
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    
    usage = psutil.disk_usage(path)
    return {
        'total': usage.total,
        'used': usage.used,
        'free': usage.free,
        'percent_used': (usage.used / usage.total) * 100 if usage.total > 0 else 0
    }
